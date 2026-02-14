from fastapi import HTTPException
from app.db.mongodb import users_collection
from app.core.security import hash_password, verify_password, create_jwt
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse

# Generate sequential user ID
async def generate_user_id() -> str:
    last_user = await users_collection.find().sort("_id", -1).limit(1).to_list(length=1)
    if not last_user:
        return "user_01"
    
    last_id = last_user[0].get("_id", "user_00")
    last_num = int(last_id.split("_")[1])
    new_num = last_num + 1
    return f"user_{new_num:02d}"

# Signup service
async def signup_user(data: UserCreate) -> UserResponse:
    existing_user = await users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(data.password)
    user_id = await generate_user_id()

    user = {"_id": user_id, "email": data.email, "hashed_password": hashed}
    await users_collection.insert_one(user)

    token = create_jwt({"email": data.email, "id": user_id})
    return UserResponse(id=user_id, email=data.email, token=token)

# Login service
async def login_user(data: UserLogin) -> UserResponse:
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_jwt({"email": user["email"], "id": user["_id"]})
    return UserResponse(id=user["_id"], email=user["email"], token=token)