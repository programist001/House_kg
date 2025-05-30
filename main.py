from fastapi import FastAPI
from house_app.api.endpoints import predict
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
    yield
    await redis_client.close()

app = FastAPI(title="House Price API", lifespan=lifespan)


app.include_router(predict.predict_router, tags=["Predicts"])

# Run app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
