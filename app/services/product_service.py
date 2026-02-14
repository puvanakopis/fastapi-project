from fastapi import HTTPException
from app.db.mongodb import products_collection
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse

# -------------- Generate sequential product ID --------------
async def generate_product_id() -> str:
    last_product = await products_collection.find().sort("_id", -1).limit(1).to_list(length=1)
    if not last_product:
        return "product_01"
    last_id = last_product[0].get("_id", "product_00")
    last_num = int(last_id.split("_")[1])
    new_num = last_num + 1
    return f"product_{new_num:02d}"

# -------------- Create product --------------
async def create_product(data: ProductCreate, save_images: bool = True) -> ProductResponse:
    product_id = await generate_product_id()
    product_dict = {"_id": product_id, **data.dict()}
    if not save_images:
        product_dict["images"] = []
    await products_collection.insert_one(product_dict)
    return ProductResponse(id=product_id, **data.dict())