from fastapi import FastAPI, Depends, Header, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from pathlib import Path
import secrets, os
from app.database import Base,engine,get_db
from app.models import Signal
from app.schemas import SignalIn
from app.config import settings
from app.analysis import analyze
from app.notify import telegram
app=FastAPI(title="POAI Phase 3",version="3.0.0",description="Pocket Option screenshot analysis assistant; no broker execution")
Base.metadata.create_all(bind=engine)
Path(settings.upload_dir).mkdir(parents=True,exist_ok=True)
app.mount('/static',StaticFiles(directory='app/static'),name='static')
def auth(x_api_key:str|None=Header(default=None)):
 if not x_api_key or not secrets.compare_digest(x_api_key,settings.api_key):raise HTTPException(401,"Invalid API key")
@app.get('/',response_class=HTMLResponse)
def home():return Path('app/templates/index.html').read_text(encoding='utf-8')
@app.get('/health')
def health():return {"status":"ok","service":"POAI","version":"3.0.0"}
@app.get('/api/signals')
def signals(limit:int=50,db:Session=Depends(get_db),_:None=Depends(auth)):
 rows=db.scalars(select(Signal).order_by(Signal.created_at.desc()).limit(max(1,min(limit,200)))).all()
 return [{"id":x.id,"created_at":x.created_at,"asset":x.asset,"market_type":x.market_type,"timeframe":x.timeframe,"side":x.side,"pattern":x.pattern,"confidence":x.confidence,"entry_zone":x.entry_zone,"rationale":x.rationale,"outcome":x.outcome,"screenshot_path":x.screenshot_path} for x in rows]
@app.post('/api/signals')
async def create_signal(payload:SignalIn,db:Session=Depends(get_db),_:None=Depends(auth)):
 x=Signal(**payload.model_dump());db.add(x);db.commit();db.refresh(x)
 if x.side!="NO TRADE" and x.confidence>=settings.confidence_threshold:
  await telegram(f"POAI ALERT\n{x.asset} [{x.market_type}] {x.timeframe}\n{x.side} | confidence {x.confidence:.0%}\nPattern: {x.pattern}\nEntry: {x.entry_zone}\n{ x.rationale }\nVisual AI estimate only; verify manually.")
 return {"id":x.id,"status":"stored"}
@app.post('/api/analyze')
async def analyze_screen(asset:str="EURUSD",market_type:str="OTC",timeframe:str="M1",file:UploadFile=File(...),db:Session=Depends(get_db),_:None=Depends(auth)):
 data=await file.read(settings.max_upload_mb*1024*1024+1)
 if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"Screenshot exceeds upload limit")
 try: result=analyze(data)
 except ValueError as e:raise HTTPException(400,str(e))
 name=f"{secrets.token_hex(12)}.jpg";path=Path(settings.upload_dir)/name
 import cv2,numpy as np
 image=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR);cv2.imwrite(str(path),image)
 s=Signal(asset=asset,market_type=market_type,timeframe=timeframe,side=result['side'],pattern=result['pattern'],confidence=result['confidence'],entry_zone=result['entry_zone'],rationale=result['rationale'],screenshot_path=name)
 db.add(s);db.commit();db.refresh(s)
 if s.side!='NO TRADE' and s.confidence>=settings.confidence_threshold:await telegram(f"POAI ALERT\n{asset} [{market_type}] {timeframe}\n{s.side} | {s.confidence:.0%}\n{s.pattern}\n{s.rationale}\nVisual estimate only; verify manually.")
 return {"signal_id":s.id,**result}
