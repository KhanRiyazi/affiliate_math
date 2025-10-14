from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    plan = Column(String, default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class AffiliateLink(Base):
    __tablename__ = "affiliate_links"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    destination_url = Column(Text)
    short_code = Column(String, unique=True, index=True)
    short_url = Column(String)
    user_id = Column(Integer, index=True)
    category = Column(String, default="affiliate")
    status = Column(String, default="active")
    clicks = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ClickEvent(Base):
    __tablename__ = "click_events"
    
    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, index=True)
    ip_address = Column(String)
    user_agent = Column(Text)
    referrer = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class RevenueEvent(Base):
    __tablename__ = "revenue_events"
    
    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, index=True)
    amount = Column(Float)
    currency = Column(String, default="USD")
    transaction_id = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())