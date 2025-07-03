# src/db/models.py
# SQLAlchemy модели для хранения позиций аукциона
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from db.session import engine
import datetime

Base = declarative_base()

class AuctionItem(Base):
    __tablename__ = "auction_items"
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, nullable=False)  # id с сайта
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    current_price = Column(Float)
    average_price = Column(Float)
    start_price = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
