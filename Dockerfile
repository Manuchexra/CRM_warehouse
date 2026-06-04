# ---- 1-bosqich: Frontend build (Node.js) ----
FROM node:18 AS frontend-builder
WORKDIR /frontend
# Frontend dependency’larni nusxalash
COPY frontend/package*.json ./
RUN npm install
# Frontend manba kodlarini nusxalash va build qilish
COPY frontend/ .
RUN npm run build   # Build natijasi odatda /frontend/dist yoki /frontend/build bo‘ladi

# ---- 2-bosqich: Backend build (Python) ----
FROM python:3.11-slim AS backend-builder
WORKDIR /backend
# Backend dependency’larni nusxalash
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Backend kodlarini nusxalash
COPY backend/ .

# ---- 3-bosqich: Yakuniy konteyner ----
FROM python:3.11-slim
WORKDIR /app

# Backend va uning kutubxonalarini ko‘chirish
COPY --from=backend-builder /backend /app/backend
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Frontend build natijasini statik papkaga ko‘chirish (masalan, /app/static)
COPY --from=frontend-builder /frontend/dist /app/static

# Backendda statik fayllarni serve qilish uchun (agar FastAPI ishlatsangiz)
# main.py faylingizda quyidagi qator bo‘lishi kerak:
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Port va CMD
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]