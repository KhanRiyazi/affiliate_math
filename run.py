import uvicorn
import os

if __name__ == "__main__":
    # Use Render's assigned port or default to 8000 for local dev
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",  # Path to your FastAPI app
        host="0.0.0.0",  # Listen on all interfaces
        port=port,
        reload=os.environ.get("RENDER", "0") != "1",  # Disable reload on Render
        log_level="info",
        access_log=True
    )
