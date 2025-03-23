from fasthtml.common import *

def inventory_page():
    return Div(
        H1("Inventory Management"),
        P("Monitor and update stock levels here."),
        Div(id="inventory-data", cls="inventory-container"),
        cls="inventory-container"
    )
