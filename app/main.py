import logging
import os

import pymysql
import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="DevOps Lab")
logger = logging.getLogger("uvicorn.error")

cache = redis.Redis(
    host="redis",
    port=6379,
    socket_connect_timeout=2,
    socket_timeout=2,
)


@app.get("/")
def index():
    return {"message": "DevOps Lab works"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    checks = {}

    try:
        connection = pymysql.connect(
            host="db",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            connect_timeout=2,
            read_timeout=2,
            write_timeout=2,
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                checks["mysql"] = cursor.fetchone()[0] == 1
        finally:
            connection.close()
    except Exception:
        logger.exception("MySQL check failed")
        checks["mysql"] = False

    try:
        checks["redis"] = bool(cache.ping())
    except Exception:
        logger.exception("Redis check failed")
        checks["redis"] = False

    success = all(checks.values())
    return JSONResponse(
        status_code=200 if success else 503,
        content={"ready": success, "checks": checks},
    )
