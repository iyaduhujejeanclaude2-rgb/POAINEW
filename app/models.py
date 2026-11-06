from sqlalchemy import String, Float, DateTime, Text, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
class Signal(Base):
 __tablename__="signals"
 id:Mapped[int]=mapped_column(primary_key=True)
 created_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)
 asset:Mapped[str]=mapped_column(String(40),index=True)
 market_type:Mapped[str]=mapped_column(String(12),default="OTC",index=True)
 timeframe:Mapped[str]=mapped_column(String(8),default="M1")
 side:Mapped[str]=mapped_column(String(12),index=True)
 pattern:Mapped[str]=mapped_column(String(120),default="")
 confidence:Mapped[float]=mapped_column(Float,default=0)
 entry_zone:Mapped[str]=mapped_column(String(120),default="visual estimate")
 rationale:Mapped[str]=mapped_column(Text,default="")
 screenshot_path:Mapped[str]=mapped_column(String(300),default="")
 reviewed:Mapped[bool]=mapped_column(Boolean,default=False)
 outcome:Mapped[str]=mapped_column(String(12),default="PENDING")
