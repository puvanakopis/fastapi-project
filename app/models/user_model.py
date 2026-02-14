from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    id: Optional[str]
    email: str
    hashed_password: str
