from typing import List, Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    name: str
    gender: str
    sizes: List[str]

class ProductCreate(ProductBase):
    images: List[str] 

class ProductUpdate(BaseModel):
    title: Optional[str]
    name: Optional[str]
    gender: Optional[str]
    sizes: Optional[List[str]]
    images: Optional[List[str]]

class ProductResponse(ProductBase):
    id: str
    images: List[str]