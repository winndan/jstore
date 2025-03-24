from datetime import datetime, timezone
from fasthtml.common import *
from monsterui.all import *
from homepage import homepage
from pages.sales import sales_page
from pages.add_products import add_products_page, save_product, upload_image, Product
from pages.credit import credit_page
from pages.reports import reports_page
from pages.inventory import inventory_page
from pages.customers import customers_page
from db_con import get_supabase_client
from pydantic import ValidationError

# ✅ Supabase Configuration
supabase = get_supabase_client()

app, rt = fast_app(hdrs=Theme.violet.headers(daisy=True), live=True)

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

@rt("/api/products/add", methods=["POST"])
def add_product(name: str, category: str, price: float, stock: int, image: File = None):
    try:
        now_utc = datetime.now(timezone.utc).isoformat()

        # ✅ Debug: Check if image is received
        if image:
            print(f"📷 Received Image: {image.filename}")
            image_id = upload_image(image, "product-images")  # ✅ Upload the file
        else:
            print("🚨 No Image Received!")
            image_id = ""

        product = Product(
            name=name,
            category=category,
            price=price,
            stock=stock,
            image_id=image_id,
            created_at=now_utc,
            updated_at=now_utc,
        )

        response = supabase.table("products").insert(product.model_dump()).execute()
        data = response.data if hasattr(response, "data") else response[1]
        count = len(data) if isinstance(data, list) else 0

        if count > 0:
            print("✅ Product added successfully!", data)
            return Div("✅ Product added successfully!", cls="success-message")  # ✅ Show message
        else:
            print("🚨 Error: No rows were inserted.")
            return Div("🚨 Failed to add product.", cls="error-message")

    except ValidationError as e:
        print("🚨 Validation Error:", e.json())
        return Div("🚨 Validation Error.", cls="error-message")
    except Exception as e:
        print(f"🚨 An error occurred: {str(e)}")
        return Div(f"🚨 Error: {str(e)}", cls="error-message")

@rt("/api/products")
def get_products(category: str = ""):
    try:
        query = supabase.table("products").select("name, price, stock, category, image_id")

        if category:
            query = query.eq("category", category)

        response = query.execute()
        data = response.data if hasattr(response, "data") else response[1]

        return Div(
            *[
                Div(
                    Div(
                        Img(src=product["image_id"], alt=product["name"], cls="product-image"),
                        cls="product-card"
                    ),
                    H3(product["name"]),
                    P(f"${product['price']}", cls="price"),
                    Button(I(cls="fas fa-plus"), cls="add-button"),
                    cls="product-card"
                )
                for product in data
            ],
            cls="products-grid"
        )

    except Exception as e:
        print(f"🚨 Error fetching products: {str(e)}")
        return Div("🚨 Error fetching products", cls="error-message")


    


if __name__ == "__main__":
    serve()
