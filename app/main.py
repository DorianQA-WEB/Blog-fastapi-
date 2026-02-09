import time
from contextlib import asynccontextmanager
from venv import logger

import logging
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

from app.core.database import create_db_and_tables
from app.modules.categories import routers as categories_routers
from app.modules.posts import routers as posts_routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается. Создаем базу данных...")
    await create_db_and_tables()
    print("База данных создана.")
    yield
    print("Приложение завершает работу.")

app = FastAPI(
    title="Простой Блог на FastAPI с SQLAlchemy",
    lifespan=lifespan,
)

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
)

app.include_router(categories_routers.router)
app.include_router(posts_routers.router)

logger = logging.getLogger("test")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    try:
        # Передаем запрос дальше в приложение
        response = await call_next(request)
        process_time = time.time() - start_time
        # Выбор уровня логирования в зависимости от статуса
        if response.status_code >= 500:
            log_func = logger.error
        elif response.status_code >= 400:
            log_func = logger.warning
        else:
            log_func = logger.info
        # Логируем успешный запрос
        log_func(
            f"Request_completed:{request.method} {request.url}"
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        return response
        # Логируем ошибку
    except Exception as e:
        # Логируем ошибку
        process_time = time.time() - start_time
        logger.exception(
            f"Request failed: {request.method} {request.url} - " f"Error: {str(e)} - " f"Time: {process_time:.3f}s"
        )

        # Возвращаем ответ с ошибкой
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Простой Блог на FastAPI с SQLAlchemy"}

#Пример эндпоинта, который вызывает ошибку
@app.get("/error")
async def trigger_error():
    raise HTTPException(
        status_code=400,
        detail="This is a test error"
    )

