from fastapi.middleware.cors import CORSMiddleware
from .main import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # "*" означает, что мы разрешаем запросы с ЛЮБОГО фронтенда (удобно для локальной разработки)
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"], # Разрешаем любые заголовки
)