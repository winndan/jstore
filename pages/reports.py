from fasthtml.common import *

def reports_page():
    return Div(
        H1("Reports & Bookkeeping"),
        P("View sales reports and financial records here."),
        Div(id="report-data", cls="reports-container"),
        cls="reports-container"
    )
