from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
import datetime
from config import DATABASE_URL

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    username = Column(String)
    language = Column(String, default="RU")
    status_paid = Column(Boolean, default=False)
    paid_at = Column(DateTime, nullable=True)
    plan_id = Column(Integer, ForeignKey("plans.plan_id"))

class Plan(Base):
    __tablename__ = "plans"
    plan_id = Column(Integer, primary_key=True)
    name = Column(String)
    stars_price = Column(Float)
    duration_days = Column(Integer)

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount_stars = Column(Float)
    currency = Column(String)
    amount_crypto = Column(Float)
    wallet_address = Column(String)
    tx_hash = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)
