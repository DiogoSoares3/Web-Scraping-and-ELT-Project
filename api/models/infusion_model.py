from sqlalchemy import Column, String, Float, DateTime, inspect, PrimaryKeyConstraint

from core.configs import settings
from core.database import engine


inspector = inspect(engine)

if 'price_over_time_infusion' in inspector.get_view_names(schema='dev'):
    class PriceOverTimeInfusion(settings.DBBaseModel):
        __tablename__ = 'price_over_time_infusion'
        __table_args__ = (PrimaryKeyConstraint('name', 'datetime'), {'schema': 'dev'})

        name: str = Column(String, nullable=False)
        price: float = Column(Float, nullable=False)
        site: str = Column(String, nullable=False)
        datetime = Column(DateTime, nullable=False)
else:
    print("Table 'price_over_time_infusion' still not exists.")
