FROM python:3.11-slim

WORKDIR /app

# Backend dependency’larni o‘rnatish
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend kodini nusxalash - BUTUN backend papkasini emas, faqat app papkasini
COPY backend/app ./app

# Frontend statik fayllarni nusxalash
COPY frontend ./static

EXPOSE 8000

# ASGI server: app.main:app (chunki biz ./app papkasiga ko‘chirdik)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]