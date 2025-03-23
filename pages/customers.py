from fasthtml.common import *

def customers_page():
    return Div(
        H1("Customers Management"),
        P("Manage your customers and their details."),
        Div(id="customers-data", cls="customers-container"),
        cls="customers-container"
    )
