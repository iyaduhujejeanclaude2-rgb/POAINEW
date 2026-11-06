"""Desktop screenshot sender: runs on the PC displaying Pocket Option chart.
This client sends captured screenshots to your hosted POAI API; crop/select screen as needed.
"""
import argparse,time,io,os
import mss
from PIL import Image
import requests
def main():
 p=argparse.ArgumentParser();p.add_argument('--api',required=True,help='https://your-domain/api/analyze');p.add_argument('--key',required=True);p.add_argument('--asset',default='EURUSD');p.add_argument('--market',choices=['OTC','STANDARD'],default='OTC');p.add_argument('--timeframe',default='M1');p.add_argument('--monitor',type=int,default=1);p.add_argument('--interval',type=float,default=3);p.add_argument('--once',action='store_true');a=p.parse_args()
 with mss.mss() as sct:
  while True:
   shot=sct.grab(sct.monitors[a.monitor]);buf=io.BytesIO();Image.frombytes('RGB',shot.size,shot.rgb).save(buf,format='JPEG',quality=85)
   try:
    r=requests.post(a.api,headers={'X-API-Key':a.key},data={'asset':a.asset,'market_type':a.market,'timeframe':a.timeframe},files={'file':('screen.jpg',buf.getvalue(),'image/jpeg')},timeout=25);print(r.status_code,r.text[:800])
   except requests.RequestException as e:print('Network error:',e)
   if a.once:break
   time.sleep(max(1,a.interval))
if __name__=='__main__':main()
