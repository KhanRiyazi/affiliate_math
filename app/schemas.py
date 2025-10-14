from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    plan: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Affiliate Link Schemas
class AffiliateLinkBase(BaseModel):
    title: str
    destination_url: str
    category: str = "affiliate"

class AffiliateLinkCreate(AffiliateLinkBase):
    pass

class AffiliateLink(AffiliateLinkBase):
    id: int
    short_code: str
    short_url: str
    user_id: int
    status: str
    clicks: int
    revenue: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Click Event Schemas
class ClickEventBase(BaseModel):
    link_id: int

class ClickEventCreate(ClickEventBase):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

class ClickEvent(ClickEventBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# Revenue Event Schemas
class RevenueEventBase(BaseModel):
    link_id: int
    amount: float

class RevenueEventCreate(RevenueEventBase):
    currency: str = "USD"
    transaction_id: Optional[str] = None

class RevenueEvent(RevenueEventBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# Dashboard Stats
class DashboardStats(BaseModel):
    total_links: int
    total_clicks: int
    total_revenue: float
    active_campaigns: int
    conversion_rate: float

# Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response Models
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class LinkStats(BaseModel):
    link_id: int
    title: str
    clicks: int
    revenue: float
    conversion_rate: float