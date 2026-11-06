from pydantic import BaseModel, Field
from typing import Literal
class SignalIn(BaseModel):
 asset:str=Field(min_length=2,max_length=40)
 market_type:Literal["OTC","STANDARD"]="OTC"
 timeframe:str="M1"
 side:Literal["BUY","SELL","NO TRADE"]
 pattern:str=""
 confidence:float=Field(ge=0,le=1)
 entry_zone:str="visual estimate"
 rationale:str=""
