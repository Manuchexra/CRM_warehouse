from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.database import engine, Base
from .routers import (
    auth_router, users_router, crm_router,
    erp_router, wms_router, reports_router
)
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(crm_router)
app.include_router(erp_router)
app.include_router(wms_router)
app.include_router(reports_router)

# ----------------------------
# STATIK FRONTEND (HTML/CSS/JS)
# ----------------------------
static_dir = Path(__file__).parent / "static"   # /app/app/static

if static_dir.exists() and static_dir.is_dir():
    # CSS va JS papkalarini mount qilish (agar mavjud bo‘lsa)
    css_dir = static_dir / "css"
    if css_dir.exists() and css_dir.is_dir():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    
    js_dir = static_dir / "js"
    if js_dir.exists() and js_dir.is_dir():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    
    # Asosiy sahifa – index.html ni ko‘rsatish
    @app.get("/", include_in_schema=False)
    async def root_html():
        index_path = static_dir / "index.html"
        if index_path.exists() and index_path.is_file():
            return FileResponse(index_path)
        return {"message": "API ishlayapti, lekin index.html topilmadi", "docs": "/docs"}
    
    # Boshqa barcha statik fayllar (masalan, dashboard.html, crm.html)
    @app.get("/{file_path:path}")
    async def serve_static_file(file_path: str):
        full_path = static_dir / file_path
        if full_path.exists() and full_path.is_file():
            return FileResponse(full_path)
        return {"error": "Fayl topilmadi"}, 404
else:
    @app.get("/")
    def root():
        return {"message": "Static papkasi mavjud emas", "docs": "/docs"}

# Debug endpoint – statik papka tarkibini tekshirish uchun
@app.get("/debug-static")
def debug_static():
    if static_dir.exists():
        files = [f.name for f in static_dir.iterdir() if f.is_file()]
        dirs = [f.name for f in static_dir.iterdir() if f.is_dir()]
        return {
            "static_dir_exists": True,
            "path": str(static_dir),
            "files": files,
            "subdirs": dirs,
        }
    else:
        return {
            "static_dir_exists": False,
            "path": str(static_dir),
            "parent_contents": [str(p) for p in Path(__file__).parent.iterdir()]
        }

@app.get("/health")
def health_check():
    return {"status": "healthy"}