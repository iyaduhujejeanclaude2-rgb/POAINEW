"""Conservative visual candle heuristics. No price feed is inferred from pixels."""
import cv2, numpy as np
def analyze(image_bytes:bytes):
 arr=np.frombuffer(image_bytes,np.uint8); img=cv2.imdecode(arr,cv2.IMREAD_COLOR)
 if img is None: raise ValueError("Invalid image; expected PNG/JPEG screenshot")
 h,w=img.shape[:2]
 # chart area heuristic: exclude lower toolbar and outer browser header
 crop=img[int(h*.12):int(h*.82),int(w*.08):int(w*.94)]
 hsv=cv2.cvtColor(crop,cv2.COLOR_BGR2HSV)
 # Common green/red candle hues; visual only, chart theme can affect detection
 green=cv2.inRange(hsv,np.array([35,45,45]),np.array([95,255,255]))
 red=cv2.bitwise_or(cv2.inRange(hsv,np.array([0,50,50]),np.array([12,255,255])),cv2.inRange(hsv,np.array([165,50,50]),np.array([180,255,255])))
 g=int(cv2.countNonZero(green)); r=int(cv2.countNonZero(red)); total=g+r
 if total<max(120,int(crop.size/1200)): return {"side":"NO TRADE","confidence":0.0,"pattern":"INSUFFICIENT_VISUAL_CANDLES","entry_zone":"Not available","rationale":"Chart candle colors could not be reliably isolated. Adjust chart crop/theme and retry."}
 imbalance=abs(g-r)/total
 side="BUY" if g>r else "SELL" if r>g else "NO TRADE"
 confidence=min(.62, .42+imbalance*.35) # capped; this is not trained prediction
 if imbalance<.12: side="NO TRADE"; confidence=.40
 return {"side":side,"confidence":round(confidence,3),"pattern":"COLOR_IMBALANCE_HEURISTIC","entry_zone":"Visual estimate only; price not decoded","rationale":f"Green pixel share {g/total:.2%}; red pixel share {r/total:.2%}. Directional color imbalance is a weak cue and cannot confirm entry."}
