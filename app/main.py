"""Точка входа FastAPI-приложения магазина «Pixel»."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pathlib

from app.routers import products, orders, analytics, customers, employees, suppliers, categories

app = FastAPI(title="Компьютерный магазин «Pixel»", version="1.0.0")

# CORS
app.add_middleware(GZipMiddleware, minimum_size=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-роутеры
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(analytics.router)
app.include_router(customers.router)
app.include_router(employees.router)
app.include_router(suppliers.router)
app.include_router(categories.router)

# Статика и SPA index.html
STATIC = pathlib.Path(__file__).parent / "static"
TEMPLATES = pathlib.Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "service": "pixel-shop"}



