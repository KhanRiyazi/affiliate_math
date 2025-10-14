from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os
import json

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LinkFlow Pro API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the frontend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)
frontend_dir = os.path.join(project_root, "frontend")

print(f"🔍 Frontend directory: {frontend_dir}")
print(f"🔍 Project root: {project_root}")

# Create frontend directory if it doesn't exist
os.makedirs(frontend_dir, exist_ok=True)
os.makedirs(os.path.join(frontend_dir, "css"), exist_ok=True)
os.makedirs(os.path.join(frontend_dir, "js"), exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# In-memory user session (for demo purposes)
current_user_id = 1  # Demo user ID

# Create demo user and links on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Create demo user if not exists
        demo_user = crud.get_user_by_email(db, email="demo@linkflow.pro")
        if not demo_user:
            user_data = schemas.UserCreate(
                email="demo@linkflow.pro",
                username="demo",
                password="demo123"
            )
            crud.create_user(db=db, user=user_data)
            print("✅ Demo user created")
        
        # Create some demo links if none exist
        user_links = crud.get_user_links(db, user_id=current_user_id)
        if not user_links:
            demo_links = [
                schemas.AffiliateLinkCreate(
                    title="Amazon Summer Sale",
                    destination_url="https://amazon.com",
                    category="affiliate"
                ),
                schemas.AffiliateLinkCreate(
                    title="Tech Gadgets Affiliate",
                    destination_url="https://bestbuy.com",
                    category="affiliate"
                ),
                schemas.AffiliateLinkCreate(
                    title="Fitness Equipment Promo",
                    destination_url="https://example.com/fitness",
                    category="affiliate"
                )
            ]
            for link_data in demo_links:
                crud.create_affiliate_link(db=db, link=link_data, user_id=current_user_id)
            print("✅ Demo links created")
        
        print("✅ Database initialized successfully")
        
        # Print available routes
        print("🌐 Available routes:")
        print("   http://localhost:8000/ - Landing page")
        print("   http://localhost:8000/dashboard - Dashboard")
        print("   http://localhost:8000/api/docs - API Documentation")
        print("   http://localhost:8000/health - Health check")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
    finally:
        db.close()

# Serve frontend files
@app.get("/")
async def read_root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        # Return a simple HTML response if index.html doesn't exist
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>LinkFlow Pro</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #0f172a; color: white; }
                .container { max-width: 800px; margin: 0 auto; text-align: center; }
                .logo { font-size: 3em; font-weight: bold; background: linear-gradient(135deg, #4361ee, #7209b7); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                .links { margin: 20px 0; }
                .links a { display: inline-block; margin: 10px; padding: 12px 24px; background: #4361ee; 
                          color: white; text-decoration: none; border-radius: 8px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">LinkFlow Pro</div>
                <h1>Affiliate Link Management SaaS</h1>
                <p>Your backend is running! Frontend files are missing.</p>
                <div class="links">
                    <a href="/dashboard">Go to Dashboard</a>
                    <a href="/api/docs">API Documentation</a>
                    <a href="/health">Health Check</a>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(html_content)

@app.get("/dashboard")
async def read_dashboard():
    dashboard_path = os.path.join(frontend_dir, "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        # Return a simple dashboard if file doesn't exist
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard - LinkFlow Pro</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: white; }
                .sidebar { width: 250px; height: 100vh; background: #1e293b; padding: 20px; float: left; }
                .main { margin-left: 250px; padding: 20px; }
                .logo { font-size: 1.5em; font-weight: bold; margin-bottom: 30px; }
                .nav a { display: block; padding: 10px; color: #94a3b8; text-decoration: none; }
                .nav a.active { color: white; background: #4361ee; border-radius: 5px; }
                .metric { background: #1e293b; padding: 20px; border-radius: 8px; margin: 10px; display: inline-block; width: 200px; }
            </style>
        </head>
        <body>
            <div class="sidebar">
                <div class="logo">LinkFlow Pro</div>
                <div class="nav">
                    <a href="#" class="active">Dashboard</a>
                    <a href="#">My Links</a>
                    <a href="#">Analytics</a>
                </div>
            </div>
            <div class="main">
                <h1>Dashboard</h1>
                <p>Backend is working! Frontend dashboard file is missing.</p>
                <div class="metric">
                    <h3>Total Links</h3>
                    <div id="totalLinks">Loading...</div>
                </div>
                <div class="metric">
                    <h3>Total Clicks</h3>
                    <div id="totalClicks">Loading...</div>
                </div>
            </div>
            <script>
                // Load stats from API
                fetch('/dashboard/stats')
                    .then(r => r.json())
                    .then(stats => {
                        document.getElementById('totalLinks').textContent = stats.total_links;
                        document.getElementById('totalClicks').textContent = stats.total_clicks;
                    });
            </script>
        </body>
        </html>
        """
        return HTMLResponse(html_content)

# Import HTMLResponse
from fastapi.responses import HTMLResponse

# API Routes (keep all your existing API endpoints)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/links/", response_model=schemas.AffiliateLink)
def create_link(link: schemas.AffiliateLinkCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_affiliate_link(db=db, link=link, user_id=current_user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating link: {str(e)}")

@app.get("/links/", response_model=List[schemas.AffiliateLink])
def read_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    links = crud.get_user_links(db, user_id=current_user_id, skip=skip, limit=limit)
    return links

@app.get("/links/{link_id}", response_model=schemas.AffiliateLink)
def read_link(link_id: int, db: Session = Depends(get_db)):
    link = crud.get_link_by_id(db, link_id=link_id)
    if link is None or link.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@app.delete("/links/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db)):
    success = crud.delete_link(db, link_id=link_id, user_id=current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Link deleted successfully"}

@app.get("/r/{short_code}")
def redirect_link(short_code: str, request: Request, db: Session = Depends(get_db)):
    link = crud.get_link_by_short_code(db, short_code=short_code)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    click_data = schemas.ClickEventCreate(
        link_id=link.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer")
    )
    crud.create_click_event(db, click=click_data)
    crud.update_link_clicks(db, link_id=link.id)
    
    return RedirectResponse(url=link.destination_url)

@app.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db, user_id=current_user_id)
    return stats

@app.get("/links/{link_id}/stats")
def get_link_stats(link_id: int, db: Session = Depends(get_db)):
    stats = crud.get_link_stats(db, link_id=link_id, user_id=current_user_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return stats

@app.post("/revenue/")
def track_revenue(revenue: schemas.RevenueEventCreate, db: Session = Depends(get_db)):
    link = crud.get_link_by_id(db, link_id=revenue.link_id)
    if link is None or link.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Link not found")
    
    crud.update_link_revenue(db, link_id=revenue.link_id, amount=revenue.amount)
    
    db_revenue = models.RevenueEvent(
        link_id=revenue.link_id,
        amount=revenue.amount,
        currency=revenue.currency,
        transaction_id=revenue.transaction_id
    )
    db.add(db_revenue)
    db.commit()
    db.refresh(db_revenue)
    
    return {"message": "Revenue tracked successfully"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "LinkFlow Pro API",
        "version": "1.0.0",
        "frontend_directory": frontend_dir,
        "frontend_exists": os.path.exists(frontend_dir)
    }

@app.get("/api")
def api_root():
    return {
        "message": "LinkFlow Pro API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "links": "/links",
            "dashboard": "/dashboard/stats"
        }
    }

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        user_count = db.query(models.User).count()
        link_count = db.query(models.AffiliateLink).count()
        return {
            "database": "working",
            "users": user_count,
            "links": link_count
        }
    except Exception as e:
        return {"database": "error", "message": str(e)}