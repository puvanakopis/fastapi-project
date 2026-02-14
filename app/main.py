from fastapi import FastAPI
from app.routers import user_routers , product_routers

app = FastAPI()

app.include_router(user_routers.router)
app.include_router(product_routers.router)

@app.get("/")
def root():
    return {"message": "FastAPI Running"}