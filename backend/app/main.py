from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.database import engine, Base
from .routers import (
    auth_router, users_router, crm_router,
    erp_router, wms_router, reports_router
)
import os
from pathlib import Path

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wholesale Clothing Management Platform API",
    description="ERP, CRM, WMS System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(crm_router)
app.include_router(erp_router)
app.include_router(wms_router)
app.include_router(reports_router)

# --- Statik frontend (HTML/CSS/JS) ---
# Konteyner ichida /app/static papkasiga ishora
static_dir = Path(__file__).parent / "static"

if static_dir.exists() and static_dir.is_dir():
    # CSS papkasini ulash
    css_dir = static_dir / "css"
    if css_dir.exists() and css_dir.is_dir():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    
    # JS papkasini ulash
    js_dir = static_dir / "js"
    if js_dir.exists() and js_dir.is_dir():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    
    # Asosiy sahifa
    @app.get("/", include_in_schema=False)
    async def root_html():
        index_path = static_dir / "index.html"
        if index_path.exists() and index_path.is_file():
            return FileResponse(index_path)
        return {"message": "API ishlayapti", "docs": "/docs", "version": "1.0.0"}
    
    # Boshqa statik fayllar (masalan, about.html, images)
    @app.get("/{file_path:path}")
    async def serve_static_file(file_path: str):
        full_path = static_dir / file_path
        if full_path.exists() and full_path.is_file():
            return FileResponse(full_path)
        return {"error": "Not found"}, 404
else:
    @app.get("/")
    def root():
        return {
            "message": "Wholesale Clothing Management Platform API",
            "docs": "/docs",
            "version": "1.0.0"
        }

@app.get("/health")
def health_check():
    return {"status": "healthy"}