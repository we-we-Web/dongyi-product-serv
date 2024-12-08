from sqlalchemy.sql import insert, delete, select, update
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi import FastAPI, HTTPException
from infrastructure.database import database
from domain.product import Product

class ProductRepository:
    @staticmethod
    async def create_product(product_data: dict):
        query = select(Product).where(Product.id == product_data["id"])
        product = await database.fetch_one(query)
        if(product):
            raise HTTPException(status_code=409, detail="Product already exist")
        else:
            query = insert(Product).values(**product_data)
            product_id = await database.execute(query)
            return product_id

    @staticmethod
    async def delete_product(product_id: int):
        query = delete(Product).where(Product.id == product_id)
        result = await database.execute(query)
        if result == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return True

    @staticmethod
    async def update_product(product_id: int, update_data: dict):
        query = update(Product).where(Product.id == product_id).values(**update_data)
        result = await database.execute(query)
        if result == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return True

    @staticmethod
    async def get_product_by_id(product_id: int):
        query = select(Product).where(Product.id == product_id)
        product = await database.fetch_one(query)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    
    @staticmethod
    async def get_all_products():
        query = select(Product)
        products = await database.fetch_all(query)
        if not products:
            raise HTTPException(status_code=404, detail="There isn't any product")
        return products
    
    @staticmethod
    async def get_products_by_category(category: str):
        query = select(Product).filter(Product.categories.like(f"%{category}%"))
        products = await database.fetch_all(query)
        if not products:
            raise HTTPException(status_code=404, detail="There isn't any product in this category")
        return products
    
    @staticmethod
    async def get_products_by_name(name: str):
        query = select(Product).filter(or_(
                func.locate(name, Product.name) > 0,
                func.locate(Product.name, name) > 0
            ))
        products = await database.fetch_all(query)
        if not products:
            raise HTTPException(status_code=404, detail="There isn't any product with this name")
        return products

