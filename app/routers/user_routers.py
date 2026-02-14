from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.user_service import signup_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse)
async def signup(data: UserCreate):
    return await signup_user(data)

@router.post("/login", response_model=UserResponse)
async def login(data: UserLogin):
    return await login_user(data)