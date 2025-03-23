from fasthtml.common import Div, H1, Form, Input, Label, Button, Select, Option, H2, Link, Script  # Ensure all necessary components are imported
from monsterui.all import *
from db_con import get_supabase_client
from fastapi import UploadFile, HTTPException
from datetime import datetime
from uuid import uuid4

# ✅ Supabase Configuration
supabase = get_supabase_client()

# ✅ Hardcoded Categories
CATEGORIES = [
    "Food Items",
    "Snacks",
    "Beverages",
    "Personal Care Products",
    "Household Essentials",
    "Tobacco Products"
]

# ✅ Upload Image to Supabase Storage
async def upload_image(file_bytes: bytes, filename: str) -> str:
    try:
        bucket_name = "product-images"
        # Generate a unique filename
        file_ext = filename.split(".")[-1]
        unique_name = f"{uuid4()}.{file_ext}"

        response = supabase.storage.from_(bucket_name).upload(
            unique_name,
            file_bytes,
            {"content-type": f"image/{file_ext}"},
            upsert=True
        )

        if response.error:
            raise HTTPException(400, detail=f"Upload failed: {response.error.message}")

        return unique_name

    except Exception as e:
        raise HTTPException(500, detail=f"Image error: {str(e)}")

async def add_product(name: str, category: str, price: float, stock: int, image: UploadFile):
    # Validate input data
    if not name or not category or not price or not stock:
        raise HTTPException(status_code=400, detail="All fields are required")

    # Validate category
    if category not in CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid category selected")

    # Validate price and stock
    if price <= 0 or stock < 0:
        raise HTTPException(status_code=400, detail="Price and stock must be positive values")

    try:
        # Upload image to Supabase Storage
        image_bytes = await image.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Image file is empty")

        image_path = await upload_image(image_bytes, image.filename)

        # Save product to Supabase Database
        return await save_product(name, category, price, stock, image_path)

    except HTTPException as e:
        raise e  # Re-raise HTTPException
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# ✅ Save Product in Supabase Database
async def save_product(name: str, category: str, price: float, stock: int, image_path: str):
    response = supabase.table("products").insert({
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "image_id": image_path,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }).execute()

    if response.error:
        raise HTTPException(status_code=400, detail="Failed to add product")

    return {"message": "Product added successfully!", "image_path": image_path}

# ✅ Frontend Page for Adding Products
def add_products_page():
    return Div(
        H1("Add New Product", cls="page-title"),
        Form(
            Div(
                Label("Product Name"),
                Input(type="text", name="name", placeholder="Enter product name", required=True),
                cls="form-group"
            ),
            Div(
                Label("Category"),
                Select(
                    Option("Select a category", value="", disabled=True, selected=True),  # Placeholder option
                    *[Option(category, value=category) for category in CATEGORIES],  # Hardcoded Categories
                    name="category", required=True  # Ensure the name attribute is set
                ),
                cls="form-group"
            ),
            Div(
                Label("Price"),
                Input(type="number", name="price", placeholder="Enter price", required=True),
                cls="form-group"
            ),
            Div(
                Label("Stock"),
                Input(type="number", name="stock", placeholder="Enter stock quantity", required=True),
                cls="form-group"
            ),
            Div(
                Label("Upload Image"),
                Input(type="file", name="image", accept="image/*", required=True),  # File input for product image
                cls="form-group"
            ),
            Button("Add Product", type="submit", **{
                "hx-post": "/api/products/add",
                "hx-encoding": "multipart/form-data",
                "hx-target": "#product-list",
                "hx-on::after-request": "this.reset()"
            }, cls="submit-button"),
            cls="product-form"
        ),
        H2("Product List", cls="product-list-title"),
        Div(id="product-list", **{
            "hx-get": "/api/products",
            "hx-trigger": "load"
        }, cls="product-list"),  # Auto-loads product list

        # ✅ Include CSS file
        Link(rel="stylesheet", href="static/styles/add_products.css"),

        # ✅ Include JavaScript file
        Script(src="static/scripts/add_products.js"),
        cls="add-product-container"
    )