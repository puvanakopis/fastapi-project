import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import create_product

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_FOLDER = "uploads" 

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/", response_model=ProductResponse)
async def add_product(
    title: str = Form(...),
    name: str = Form(...),
    gender: str = Form(...),
    sizes: List[str] = Form(...),
    images: List[UploadFile] = File(...)
):
    product_data = ProductCreate(
        title=title,
        name=name,
        gender=gender,
        sizes=sizes,
        images=[]  
    )

    product_response = await create_product(product_data, save_images=False)
    product_id = product_response.id

    image_paths = []
    for idx, img in enumerate(images, start=1):
        ext = os.path.splitext(img.filename)[1] 
        filename = f"{product_id}_{idx:02d}{ext}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        image_paths.append(path)

    await update_product(product_id, ProductUpdate(
        title=title,
        name=name,
        gender=gender,
        sizes=sizes,
        images=image_paths
    ))

    return ProductResponse(
        id=product_id,
        title=title,
        name=name,
        gender=gender,
        sizes=sizes,
        images=image_paths
    )