from fasthtml.common import *
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("supa_urll")
SUPABASE_KEY = os.getenv("supa_keyy")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Fetch categories dynamically from Supabase
def fetch_categories():
    response = supabase.table("products").select("category").execute()
    categories = set(item["category"] for item in response.data)  # Unique categories
    return sorted(categories)  # Sort categories alphabetically

def sales_page():
    categories = fetch_categories()
    
    return Div(
        # ✅ Main Content Area
        Main(
            Div(
                H1("Items"),
                Div(H2("Categories", I(cls="fas fa-chevron-down")), cls="category-dropdown"),
                Div(
                    Div(I(cls="fas fa-search"), Input(type="text", placeholder="Search for items..."), cls="search-box"),
                    Button(I(cls="fas fa-sliders-h"), cls="filter-button"),
                    cls="search-container"
                ),
                # ✅ Dynamically Generated Category Tabs with HTMX
                Div(
                    *[
                        Button(category, cls="tab", **{"data-category": category, "hx-get": f"/api/products?category={category}", "hx-target": "#products-grid"})
                        for category in categories
                    ],
                    Button(I(cls="fas fa-chevron-right"), cls="tab-arrow"),
                    cls="category-tabs"
                ),
                cls="header"
            ),
            
            Div(
                Div(
                    cls="products-grid", id="products-grid", **{"hx-get": f"/api/products?category={categories[0]}", "hx-trigger": "load"}
                ),
                cls="main-content"
            ),
        ),

        # ✅ Include CSS file
        Link(rel="stylesheet", href="static/styles/sales.css"),
        
        # ✅ Include JavaScript file
        Script(src="static/scripts/sales.js"),
    )

def render_product_card(product):
    return Div(
        Div(Img(src=product["image_id"], alt=product["name"], cls="product-image"), cls="product-image-container"),
        Div(
            H3(product["name"], cls="product-title"),
            P(f"${product['price']:.2f}", cls="price"),
            Div(
                Button("Buy", cls="buy-button", **{"data-id": product["id"]}),
                Button("Restock", cls="restock-button", **{"data-id": product["id"]}),
                cls="product-actions"
            ),
            cls="product-info"
        ),
        cls="product-card"
    )
