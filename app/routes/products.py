from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from app.schema import Product


product_router = APIRouter(prefix="/products", tags=["Products"])

products = [
    Product(id=1, name="Product 1", price=10.0, description="Description 1"),
    Product(id=2, name="Product 2", price=20.0, description="Description 2"),
    Product(id=3, name="Product 3", price=30.0, description="Description 3"),
    Product(id=4, name="Product 4", price=40.0, description="Description 4"),
]


@product_router.get(path="/", response_model=list[Product])
def get_products() -> list[Product]:
    return products


@product_router.get(path="/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    for product in products:
        if product.id == product_id:
            return product

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Product not found")
