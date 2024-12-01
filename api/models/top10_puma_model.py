from sqlalchemy import Column, String, Float, inspect, PrimaryKeyConstraint

from core.configs import settings
from core.database import engine


inspector = inspect(engine)

if 'top10_best_puma_shoes_price' in inspector.get_view_names(schema='data'):
    class Top10BestPumaShoesPrice(settings.DBBaseModel):
        __tablename__ = 'top10_best_puma_shoes_price'
        __table_args__ = (PrimaryKeyConstraint('name', 'site'), {'schema': 'data'})

        name: str = Column(String, nullable=False)
        brand: str = Column(String)
        price: float = Column(Float, nullable=False)
        site: str = Column(String, nullable=False)
else:
    print("Table 'top10_best_puma_shoes_price' still not exists.")
