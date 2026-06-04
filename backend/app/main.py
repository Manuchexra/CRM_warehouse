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


# 1. Aniq route’lar
@app.get("/")
async def root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "API is running", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 2. Statik fayllar uchun mount (css, js)
if os.path.exists(os.path.join(static_dir, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(static_dir, "css")), name="css")
if os.path.exists(os.path.join(static_dir, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(static_dir, "js")), name="js")

# 3. Catch-all route (faqat fayllar uchun)
@app.get("/{file_path:path}")
async def serve_static_file(file_path: str):
    full_path = os.path.join(static_dir, file_path)
    if os.path.isfile(full_path):
        return FileResponse(full_path)
    # Agar fayl bo‘lmasa, 404 qaytar (yoki index.html – SPA bo‘lsa)
    return {"error": "Not found"}, 404