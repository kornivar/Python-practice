from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

app = FastAPI(
    title="Mini Store App",
    description="Создание интернет магазина",
    version="1.0.0",
)

products = [
    {"id": 1, "name": "Mechanical Keyboard", "category": "peripherals", "price": 89.99, "stock": 12,
     "description": "Hot-swap mechanical keyboard"},
    {"id": 2, "name": "Gaming Mouse", "category": "peripherals", "price": 49.50, "stock": 0,
     "description": "Lighweight FPS mouse"},
    {"id": 3, "name": "RTX 5070", "category": "hardware", "price": 699.00, "stock": 4,
     "description": "Desktop graphics card"},
    {"id": 4, "name": "32GB DDR5 Kit", "category": "hardware", "price": 119, "stock": 9, "description": "None"},
]


class ProductCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0, le=100_000)
    description: str | None = Field(default=None, max_length=500)

class ProductPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0, le=100_000)
    description: str | None = Field(default=None, max_length=500)


def find_product_and_validate_name(product_id: int, new_name: str | None = None) -> tuple[int, dict]:
    target_idx, target_item = None, None

    for idx, item in enumerate(products):
        if item["id"] == product_id:
            target_idx, target_item = idx, item

        if new_name and item["name"].lower() == new_name.lower() and item["id"] != product_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists"
            )

    if target_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return target_idx, target_item

@app.get("/")
def root():
    return {"message": "Mini Store App is running"}


@app.get("/products")
def get_products(
        category: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
        min_price: Annotated[float | None, Query(ge=0)] = None,
        max_price: Annotated[float | None, Query(ge=0)] = None,
        in_stock: bool | None = None,
        search: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min price cannot be greater than max price"
        )

    result = products.copy()

    if category is not None:
        result = [p for p in result if p["category"].lower() == category.lower()]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if in_stock is not None:
        if in_stock:
            result = [p for p in result if p["stock"] > 0]
        else:
            result = [p for p in result if p["stock"] == 0]

    if search is not None:
        text = search.lower()
        result = [
            p for p in result
            if text in p["name"].lower()
               or text in (p["description"] or "").lower()
        ]

    return result


@app.get("/products/{product_id}")
def get_products_by_id(product_id: int):
    _, item = find_product_and_validate_name(product_id)
    return item


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    if any(p["name"].lower() == product.name.lower() for p in products):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product name already exists"
        )

    new_id = max((item["id"] for item in products), default=0) + 1
    new_product = {
        "id": new_id,
        ** product.model_dump(),
    }

    products.append(new_product)
    return new_product


@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: ProductCreate):
    idx, _ = find_product_and_validate_name(product_id, new_name=product.name)
    updated_product = {
        "id": product_id,
        **product.model_dump(),
    }

    products[idx] = updated_product
    return updated_product

@app.patch("/products/{product_id}", status_code=status.HTTP_200_OK)
def patch_product(product_id: int, product: ProductPatch):
    update_data = product.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for partial update"
        )

    idx, item = find_product_and_validate_name(product_id, new_name=update_data.get("name"))

    updated_product = {**item, **update_data}
    products[idx] = updated_product

    return updated_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    idx, _ = find_product_and_validate_name(product_id)
    products.pop(idx)
    return

