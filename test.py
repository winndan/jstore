from supabase import create_client, Client
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Supabase credentials
# Get Supabase credentials from .env
SUPABASE_URL = "https://uiejrmqsocfhdyltdttj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVpZWpybXFzb2NmaGR5bHRkdHRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI2NDU4OTYsImV4cCI6MjA1ODIyMTg5Nn0.YEa2rv3iRaQ0YrUK_EuG6bKz2CG0P25zpPtqWsuZGi0"

# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to add a product
def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    expiration = input("Enter expiration date (YYYY-MM-DD): ")

    data = {"name": name, "price": price, "quantity": quantity, "expiration": expiration}
    response = supabase.table("products").insert(data).execute()
    print("Product added:", response)

# Function to fetch and display products
def view_products():
    response = supabase.table("products").select("*").execute()
    for product in response.data:
        print(f"{product['id']} - {product['name']} | ₱{product['price']} | Stock: {product['quantity']} | Exp: {product['expiration']}")

# Example usage
while True:
    print("\n1. Add Product\n2. View Products\n3. Exit")
    choice = input("Select option: ")
    if choice == "1":
        add_product()
    elif choice == "2":
        view_products()
    elif choice == "3":
        break
    else:
        print("Invalid choice. Try again.")
