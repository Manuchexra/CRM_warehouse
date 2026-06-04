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
    allow_origins=["*"],  # Frontend URLs
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

# --- Statik frontend (HTML/CSS/JS) uchun qo‘shimcha ---
# Statik fayllar papkasi: /app/static (Docker konteyner ichida)
static_dir = "static"
if os.path.exists(static_dir):
    # Statik resurslar (css, js, images) ni serve qilish
    app.mount("/css", StaticFiles(directory=os.path.join(static_dir, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(static_dir, "js")), name="js")
    # Agar boshqa papkalar bo'lsa (masalan, images, fonts) – shunga o‘xshab qo‘shing

    # HTML fayllarni serve qilish uchun maxsus endpoint
    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str):
        # Agar so‘ralgan fayl .html bo‘lsa yoki papka ichidagi fayl
        full_path = os.path.join(static_dir, file_path)
        if os.path.isfile(full_path):
            return FileResponse(full_path)
        # Agar so‘ralgan yo‘l HTML faylga to‘g‘ri kelmasa, indeksni qaytar (SPA uchun)
        # Agar sizda SPA bo‘lmasa, 404 qaytaring. Oddiy multi-page uchun:
        if os.path.exists(full_path):
            return FileResponse(full_path)
        # Aks holda 404
        return {"error": "Not found"}, 404

    # Asosiy sahifa: / yo‘lida index.html ni ko‘rsatish
    @app.get("/", include_in_schema=False)
    async def root_html():
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        # Agar index.html bo‘lmasa, API xabarini qaytar (eski root funksiya)
        return {"message": "Wholesale Clothing Management Platform API", "docs": "/docs", "version": "1.0.0"}
else:
    # Agar static papkasi mavjud bo‘lmasa, eski root ishlaydi
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