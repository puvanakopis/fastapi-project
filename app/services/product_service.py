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

# -------------- Get all products --------------
async def get_products():
    products = await products_collection.find().to_list(length=100)
    return [ProductResponse(
        id=p["_id"],
        title=p["title"],
        name=p["name"],
        gender=p["gender"],
        sizes=p["sizes"],
        images=p["images"]
    ) for p in products]

# -------------- Update product --------------
async def update_product(product_id: str, data: ProductUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    result = await products_collection.update_one({"_id": product_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await products_collection.find_one({"_id": product_id})
    return ProductResponse(
        id=product["_id"],
        title=product["title"],
        name=product["name"],
        gender=product["gender"],
        sizes=product["sizes"],
        images=product["images"]
    )