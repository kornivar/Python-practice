from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

# min_price: Annotated[float | None, Query(ge=0)] = None

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


@app.get("/")
def root():
    return {"message": "Mini Store App is running"}


# @app.get("/products")
# def get_products(category: str | None = None):
#     result = products.copy()

#     if category is not None:
#         result=[
#             product
#             for product in result
#             if product["category"].lower() == category.lower()
#         ]

#     return result


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
def get_products(products_id: int):
    for product in products:
        if product["id"] == products_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    new_id = max((item["id"] for item in products), default=0) + 1

    new_product = {
        "id": new_id,
        ** product.model_dump(),
    }

    products.append(new_product)
    return new_product