import os
import mimetypes
from datetime import datetime
from db_con import get_supabase_client
from pydantic import BaseModel, ValidationError
from fasthtml.common import *

# ✅ Supabase Configuration
supabase = get_supabase_client()

# ✅ Define Product Model using Pydantic
class Product(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    image_id: str = ""
    created_at: str
    updated_at: str

import os
import mimetypes
from db_con import get_supabase_client

supabase = get_supabase_client()

def upload_image(image: File, storage_bucket: str) -> str:
    try:
        if not image:
            print("🚨 No image provided!")
            return ""

        # ✅ Get filename from the uploaded image
        image_name = image.filename
        mime_type, _ = mimetypes.guess_type(image_name)

        print(f"📂 Uploading: {image_name} | MIME: {mime_type}")

        # ✅ Read the image file properly
        file_data = image.file.read()

        # ✅ Upload the file to Supabase
        response = supabase.storage.from_(storage_bucket).upload(
            f"product-images/{image_name}",
            file_data,
            {"content-type": mime_type}
        )

        print(f"📡 Upload Response: {response}")

        # ✅ Check if upload was successful
        if isinstance(response, dict) and "error" in response:
            print(f"🚨 Upload Error: {response['error']}")
            return ""

        # ✅ Get Public URL
        public_url = supabase.storage.from_(storage_bucket).get_public_url(f"product-images/{image_name}")
        print(f"✅ Upload Successful! Public URL: {public_url}")

        return public_url  # Return the public URL

    except Exception as e:
        print(f"🚨 Exception: {str(e)}")
        return ""



async def save_product(name: str, category: str, price: float, stock: int, image_path: str = None):
    try:
        image_id = upload_image(image_path, 'product-images') if image_path else ""
        now_utc = datetime.utcnow().isoformat()

        response = supabase.table("products").insert({
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "image_id": image_id,  
            "created_at": now_utc,
            "updated_at": now_utc
        }).execute()

        data, count = response  # Ensure correct unpacking

        if count == 0:
            raise Exception("🚨 Failed to add product to database")

        return {"message": "✅ Product added successfully!", "image_id": image_id}

    except ValidationError as e:
        return {"error": "🚨 Validation Error", "details": e.errors()}
    except Exception as e:
        return {"error": f"🚨 An error occurred: {str(e)}"}

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
                Input(type="text", name="category", placeholder="Enter category", required=True),
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
                Input(type="file", name="image", accept="image/*", required=True),
                cls="form-group"
            ),
            Button("Add Product", type="submit", **{
                "hx-post": "/api/products/add",
                "hx-encoding": "multipart/form-data",  # ✅ Allow file uploads
                "hx-target": "#message-box",
                "hx-swap": "innerHTML",
                "hx-on::after-request": "this.form.reset();"
            }, cls="submit-button"),
            cls="product-form"
        ),
        Div(id="message-box", cls="message-box"),  # ✅ Message Box for Response

        Link(rel="stylesheet", href="static/styles/add_products.css"),
        Script(src="static/scripts/add_products.js"),
        cls="add-product-container"
    )
