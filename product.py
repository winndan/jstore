from db_con import get_supabase_client

# Initialize the Supabase client
supabase = get_supabase_client()

def get_products(search_query=""):
    """Fetch products from Supabase"""
    query = supabase.table("products").select("*")
    if search_query:
        query = query.ilike("name", f"%{search_query}%")
    data = query.execute()
    return data.data

def add_product(name, price, stock):
    """Add a new product to Supabase"""
    data = supabase.table("products").insert({"name": name, "price": price, "stock": stock}).execute()
    return data.data
