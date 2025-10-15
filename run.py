import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))

    # Run Uvicorn server
    uvicorn.run(
        "app.main:app",  # Your FastAPI app path
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True,
        reload=False  # Disable reload for production
    )
