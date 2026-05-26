from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime, timezone
import time
import os

app = FastAPI(title="App API")

# Record the time the application starts to calculate uptime safely
START_TIME = time.time()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Homepage with a Hero Image.
    Uses an Unsplash placeholder for the background image.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Our App</title>
        <style>
            body { 
                margin: 0; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            }
            .hero {
                /* Placeholder hero image from Unsplash */
                background-image: url('https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1200&q=80');
                background-size: cover;
                background-position: center;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                text-align: center;
            }
            .hero-content {
                background-color: rgba(0, 0, 0, 0.4); /* Dark overlay for text readability */
                padding: 40px;
                border-radius: 10px;
            }
            .hero h1 { 
                font-size: 4rem; 
                margin: 0 0 10px 0; 
            }
            .hero p { 
                font-size: 1.5rem; 
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="hero">
            <div class="hero-content">
                <h1>Welcome</h1>
                <p>Your FastAPI server is up and running.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/status")
async def get_status():
    """
    Shows basic server status.
    Deliberately omits sensitive system data (like OS details, memory usage, or internal IPs).
    """
    uptime_seconds = round(time.time() - START_TIME, 2)
    return {
        "server": "online",
        "uptime_seconds": uptime_seconds,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
async def get_health():
    """
    Standard app health check for load balancers or orchestrators (e.g., Docker/Kubernetes).
    """
    return {
        "status": "ok"
    }

@app.get("/version")
async def get_version():
    """
    Shows the current application version.
    Pulls dynamically from the environment variables set by Kubernetes.
    """
    app_version = os.getenv("APP_VERSION", "1.0.0")
    return {
        "app_name": "Python App API",
        "version": app_version
    }