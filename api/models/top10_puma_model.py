from sqlalchemy import Column, String, inspect, PrimaryKeyConstraint
from core.configs import settings
from core.database import engine


inspector = inspect(engine)

if 'top_10_best_puma_shoes_price' in inspector.get_view_names(schema='data'):
    class Top10BestPumaShoesPrice(settings.DBBaseModel):
        __tablename__ = 'top_10_best_puma_shoes_price'
        __table_args__ = (PrimaryKeyConstraint('name', 'datetime'), 
                          {'autoload_with': engine, 'schema': 'data'})

        name: str = Column(String, nullable=False)
        brand: float = Column(String)
        price: str = Column(String, nullable=False)
        site: str = Column(String, nullable=False)
else:
    print("Table 'top_10_best_puma_shoes_price' still not exists.")
