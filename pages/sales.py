from fasthtml.common import *

def sales_page():
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
                Div(
                    Button("Fruits & Vegetables", cls="tab active", **{"data-category": "fruits-vegetables", "hx-get": "/api/products?category=fruits-vegetables", "hx-target": "#products-grid"}),
                    Button("Dairy", cls="tab", **{"data-category": "dairy", "hx-get": "/api/products?category=dairy", "hx-target": "#products-grid"}),
                    Button("Meat & Seafood", cls="tab", **{"data-category": "meat-seafood", "hx-get": "/api/products?category=meat-seafood", "hx-target": "#products-grid"}),
                    Button("Bakery", cls="tab", **{"data-category": "bakery", "hx-get": "/api/products?category=bakery", "hx-target": "#products-grid"}),
                    Button("Beverages", cls="tab", **{"data-category": "beverages", "hx-get": "/api/products?category=beverages", "hx-target": "#products-grid"}),
                    Button("Snacks", cls="tab", **{"data-category": "snacks", "hx-get": "/api/products?category=snacks", "hx-target": "#products-grid"}),
                    Button("Household", cls="tab", **{"data-category": "household", "hx-get": "/api/products?category=household", "hx-target": "#products-grid"}),
                    Button(I(cls="fas fa-chevron-right"), cls="tab-arrow"),
                    cls="category-tabs"
                ),
                cls="header"
            ),

            Div(
                Div(cls="products-grid", id="products-grid", **{"hx-get": "/api/products?category=fruits-vegetables", "hx-trigger": "load"}),
                cls="main-content"
            ),
        ),

        # ✅ Include CSS file
        Link(rel="stylesheet", href="static/styles/global.css"),
        
        # ✅ Include JavaScript file
        Script(src="static/scripts/sales.js"),
    )
