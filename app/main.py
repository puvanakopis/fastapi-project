from fastapi import FastAPI
from app.routers import user_routers

app = FastAPI()

app.include_router(user_routers.router)

@app.get("/")
def root():
    return {"message": "FastAPI Running"}
