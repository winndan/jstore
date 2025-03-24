from fasthtml.common import *
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure environment variables exist
SUPABASE_URL = os.getenv("supa_urll")
SUPABASE_KEY = os.getenv("supa_keyy")

# Validate credentials before proceeding
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Check your .env file.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Fetch categories dynamically from Supabase
def fetch_categories():
    try:
        response = supabase.table("products").select("category").execute()
        
        # Ensure data is not None before processing
        if response.data:
            categories = set(item["category"] for item in response.data if item.get("category"))
            return sorted(categories) if categories else ["All"]  # Default category
        
        return ["All"]  # Fallback if no data

    except Exception as e:
        print(f"Error fetching categories: {e}")
        return ["All"]  # Default category on failure

# ✅ Sales Page UI
def sales_page():
    categories = fetch_categories()
    default_category = categories[0]  # Ensure there's always a default category

    return Div(
        # ✅ Message Box for Feedback
        Div(id="message-box", cls="message-box"),
        
        # ✅ Page Header
        H2("Product List", cls="product-list-title"),
        
        # ✅ Search & Filter Section
        Div(
            Div(I(cls="fas fa-search"), Input(type="text", placeholder="Search for items...", id="search-input"), cls="search-box"),
            Button(I(cls="fas fa-sliders-h"), cls="filter-button"),
            cls="search-container"
        ),
        
        # ✅ Category Tabs
        Div(
            *[
                Button(category, cls="tab", **{
                    "data-category": category,
                    "hx-get": f"/api/products?category={category}",
                    "hx-target": "#product-list",
                    "hx-trigger": "click"
                })
                for category in categories
            ],
            cls="category-tabs"
        ),
        
        # ✅ Product List (Auto-loads Default Category)
        Div(
            id="product-list",
            **{
                "hx-get": f"/api/products?category={default_category}",
                "hx-trigger": "load"
            },
            cls="product-list"
        ),
        
        # ✅ Load Styles & Scripts
        Link(rel="stylesheet", href="static/styles/sales.css"),
        Script(src="static/scripts/sales.js"),
    )
