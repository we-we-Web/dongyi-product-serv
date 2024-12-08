from fastapi import FastAPI
from infrastructure.database import engine, database
from domain.product import Base
from fastapi.middleware.cors import CORSMiddleware
from API.product_routes import router as product_router
from API.product_image_routes import router as product_image_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        Base.metadata.create_all(bind=engine)
        print("Database connected successfully.")
    except Exception as e:
        print(f"Database connection error: {e}")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("Database disconnected successfully.")

app.include_router(product_router, prefix="/product", tags=["Products"])
app.include_router(product_image_router, prefix="/product_image", tags=["Product Images"])




