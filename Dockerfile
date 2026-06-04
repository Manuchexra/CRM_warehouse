FROM python:3.11-slim

WORKDIR /app

# Backend dependency’larni o‘rnatish
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend kodini nusxalash
COPY backend/ ./backend/

# Frontend statik fayllarni nusxalash (HTML, CSS, JS va boshqalar)
COPY frontend/ ./static/

# FastAPI da statik fayllarni serve qilish uchun (quyida main.py ga o‘zgartirish kiritamiz)
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]