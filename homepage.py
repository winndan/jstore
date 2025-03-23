from fasthtml.common import *
from monsterui.all import *

def homepage():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("FreshMart Grocery"),
            Link(rel="stylesheet", href="static/styles/global.css"),
            Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            ),
            Link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
            ),
            Script(src="https://unpkg.com/htmx.org@1.9.6"),  # ✅ HTMX for dynamic updates
        ),
        Body(
            Div(
                # ✅ Sidebar Navigation
                Nav(
                    Div(Div(I(cls="fas fa-shopping-basket"), cls="logo-circle"), cls="logo"),
                    Ul(
                        Li(I(cls="fas fa-home"), cls="nav-item active", **{
                            "hx-get": "/page-content/sales",
                            "hx-target": "#main-content",
                            "hx-on:click": "document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active')); this.classList.add('active')"
                        }),
                        Li(I(cls="fas fa-th"), cls="nav-item", **{
                            "hx-get": "/page-content/add-products",
                            "hx-target": "#main-content",
                            "hx-on:click": "document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active')); this.classList.add('active')"
                        }),
                        Li(I(cls="fas fa-bookmark"), cls="nav-item", **{
                            "hx-get": "/page-content/credit",
                            "hx-target": "#main-content",
                            "hx-on:click": "document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active')); this.classList.add('active')"
                        }),
                        Li(I(cls="fas fa-shopping-cart"), cls="nav-item", **{
                            "hx-get": "/page-content/reports",
                            "hx-target": "#main-content",
                            "hx-on:click": "document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active')); this.classList.add('active')"
                        }),
                        Li(I(cls="fas fa-comment"), cls="nav-item", **{
                            "hx-get": "/page-content/inventory",
                            "hx-target": "#main-content",
                            "hx-on:click": "document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active')); this.classList.add('active')"
                        }),
                        Li(I(cls="fas fa-users"), cls="nav-item", **{
                            "hx-get": "/page-content/customers",
                            "hx-target": "#main-content",
                            "hx-on:click": "document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active')); this.classList.add('active')"
                        }),
                        cls="nav-items",
                    ),
                    Div(
                        Div(I(cls="fas fa-cog"), cls="nav-item"),
                        Div(I(cls="fas fa-question-circle"), cls="nav-item"),
                        cls="nav-bottom",
                    ),
                    cls="sidebar",
                ),

                # ✅ Dynamic Content Wrapper (Sales page loads first)
                Main(
                    Div(id="main-content", cls="content-area", **{
                        "hx-get": "/page-content/sales",
                        "hx-trigger": "load"
                    }),
                    cls="main-content",
                ),

                # ✅ Order Summary Sidebar (Adjust width & alignment)
                Aside(
                    H2("Current Order"),
                    Div(
                        Div(Img(src="/placeholder.svg?height=40&width=40", alt="Customer Avatar"), cls="customer-avatar"),
                        P("Emma Wang", cls="customer-name"),
                        cls="customer-info",
                    ),
                    Div(id="order-items"),
                    Div(
                        Div(Span("Subtotal"), Span("£0.00"), cls="summary-row"),
                        Div(Span("Discount"), Span("£0.00"), cls="summary-row"),
                        Div(Span("Service Charge"), Span("0%"), cls="summary-row"),
                        Div(Span("Tax"), Span("£0.00"), cls="summary-row"),
                        Div(Span("Total"), Span("£0.00"), cls="summary-row total"),
                        cls="order-summary-details",
                    ),
                    Button("Continue", cls="continue-button"),
                    cls="order-summary",
                ),

                cls="app-container",
            ),

            # ✅ Include Global CSS
            Link(rel="stylesheet", href="static/styles/global.css"),
        ),
        lang="en",
    )
