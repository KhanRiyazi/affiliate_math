from sqlalchemy.orm import Session
from . import models, schemas
import secrets
import string
from datetime import datetime, timedelta

# User CRUD Operations
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # In a real app, you would hash the password
    fake_hashed_password = user.password + "_notreallyhashed"
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Affiliate Link CRUD Operations
def generate_short_code(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_affiliate_link(db: Session, link: schemas.AffiliateLinkCreate, user_id: int):
    short_code = generate_short_code()
    short_url = f"http://localhost:8000/r/{short_code}"
    
    db_link = models.AffiliateLink(
        title=link.title,
        destination_url=link.destination_url,
        category=link.category,
        user_id=user_id,
        short_code=short_code,
        short_url=short_url,
        status="active",
        clicks=0,
        revenue=0.0
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_user_links(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.AffiliateLink).filter(
        models.AffiliateLink.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_link_by_short_code(db: Session, short_code: str):
    return db.query(models.AffiliateLink).filter(
        models.AffiliateLink.short_code == short_code
    ).first()

def get_link_by_id(db: Session, link_id: int):
    return db.query(models.AffiliateLink).filter(models.AffiliateLink.id == link_id).first()

def update_link_clicks(db: Session, link_id: int):
    link = db.query(models.AffiliateLink).filter(models.AffiliateLink.id == link_id).first()
    if link:
        link.clicks += 1
        db.commit()
        db.refresh(link)
    return link

def update_link_revenue(db: Session, link_id: int, amount: float):
    link = db.query(models.AffiliateLink).filter(models.AffiliateLink.id == link_id).first()
    if link:
        link.revenue += amount
        db.commit()
        db.refresh(link)
    return link

def delete_link(db: Session, link_id: int, user_id: int):
    link = db.query(models.AffiliateLink).filter(
        models.AffiliateLink.id == link_id,
        models.AffiliateLink.user_id == user_id
    ).first()
    if link:
        db.delete(link)
        db.commit()
        return True
    return False

# Click Events
def create_click_event(db: Session, click: schemas.ClickEventCreate):
    db_click = models.ClickEvent(
        link_id=click.link_id,
        ip_address=click.ip_address,
        user_agent=click.user_agent,
        referrer=click.referrer
    )
    db.add(db_click)
    db.commit()
    db.refresh(db_click)
    return db_click

# Dashboard Stats
def get_dashboard_stats(db: Session, user_id: int):
    links = db.query(models.AffiliateLink).filter(models.AffiliateLink.user_id == user_id).all()
    
    if not links:
        return {
            "total_links": 0,
            "total_clicks": 0,
            "total_revenue": 0.0,
            "active_campaigns": 0,
            "conversion_rate": 0.0
        }
    
    total_links = len(links)
    total_clicks = sum(link.clicks for link in links)
    total_revenue = sum(link.revenue for link in links)
    active_campaigns = len([link for link in links if link.status == "active"])
    
    conversion_rate = 0.0
    if total_clicks > 0:
        # Simple conversion rate calculation
        conversion_rate = round((total_revenue / total_clicks) * 100, 2)
    
    return {
        "total_links": total_links,
        "total_clicks": total_clicks,
        "total_revenue": total_revenue,
        "active_campaigns": active_campaigns,
        "conversion_rate": conversion_rate
    }

def get_link_stats(db: Session, link_id: int, user_id: int):
    link = db.query(models.AffiliateLink).filter(
        models.AffiliateLink.id == link_id,
        models.AffiliateLink.user_id == user_id
    ).first()
    
    if not link:
        return None
    
    conversion_rate = 0.0
    if link.clicks > 0:
        conversion_rate = round((link.revenue / link.clicks) * 100, 2)
    
    return {
        "link_id": link.id,
        "title": link.title,
        "clicks": link.clicks,
        "revenue": link.revenue,
        "conversion_rate": conversion_rate
    }