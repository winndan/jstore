from fasthtml.common import *
from monsterui.all import *
from homepage import homepage
from pages.sales import sales_page
from pages.add_products import add_products_page, save_product, upload_image
from pages.credit import credit_page
from pages.reports import reports_page
from pages.inventory import inventory_page
from pages.customers import customers_page
from fastapi import UploadFile, File, Form, HTTPException
from db_con import get_supabase_client

app, rt = fast_app()

# ✅ Main UI Page
@rt("/")
def home():
    return homepage()

# ✅ API Routes for Dynamic Page Updates (HTMX)
@rt("/page-content/{page_name}")
def load_page(page_name: str):
    pages = {
        "sales": sales_page(),
        "add-products": add_products_page(),
        "credit": credit_page(),
        "reports": reports_page(),
        "inventory": inventory_page(),
        "customers": customers_page(),
    }
    return pages.get(page_name, Div(H1("Page Not Found")))

# ✅ API Endpoint: Fetch Products
@rt("/api/products")
async def api_fetch_products(category: str = None):
    return await fetch_products(category)

# ✅ API Endpoint: Add Product
@rt("/api/products/add", methods=["POST"])
async def api_add_product(
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(...)
):
    try:
        # ✅ Read file content properly
        file_bytes = await image.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Invalid file upload.")

        # ✅ Upload image to Supabase Storage
        image_id = await upload_image(file_bytes, image.filename)  # Call the upload_image function

        # ✅ Save product details to Supabase
        return await save_product(name, category, price, stock, image_id)  # Use image_id directly

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    serve()
