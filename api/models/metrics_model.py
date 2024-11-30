from sqlalchemy import Column, Float, String, Integer, inspect, PrimaryKeyConstraint
from core.configs import settings
from core.database import engine


inspector = inspect(engine)

if 'metrics_puma_prices' in inspector.get_view_names(schema='data'):
    class MetricsPumaPrices(settings.DBBaseModel):
        __tablename__ = 'metrics_puma_prices'
        __table_args__ = (PrimaryKeyConstraint('site'), {'schema': 'data'})

        site: str = Column(String, nullable=False)
        min_price: float = Column(Float, nullable=False)
        max_price: float = Column(Float, nullable=False)
        mean_price: float = Column(Float, nullable=False)
        stddev_price: float = Column(Float, nullable=False)
        percentile_25: float = Column(Float, nullable=False)
        median_price: float = Column(Float, nullable=False)
        percentile_75: float = Column(Float, nullable=False)
        qtd_shoes: float = Column(Integer, nullable=False)
else:
    print("Table 'metrics_puma_prices' still not exists.")
