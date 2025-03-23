from datetime import datetime, timezone
from db_con import get_supabase_client
from pydantic import BaseModel, ValidationError
import os

# ✅ Initialize Supabase client
supabase = get_supabase_client()

# ✅ Define Product Model using Pydantic
class Product(BaseModel):
    name: str
    category: str
    price: float
    image_id: str = None  # Optional field
    created_at: str
    updated_at: str

# ✅ Upload Image Function
def upload_image(image_path: str, storage_bucket: str) -> str:
    try:
        image_name = os.path.basename(image_path)

        # Attempt to get the public URL of the existing image
        public_url_response = supabase.storage.from_(storage_bucket).get_public_url(image_name)

        if 'publicUrl' in public_url_response:  # Ensure we check for the key
            existing_url = public_url_response['publicUrl']
            print(f"Image already exists: {existing_url}")
            return image_name  # Return the existing image name (ID)

    except Exception as e:
        # If the image does not exist, an exception will be thrown; we can ignore this.
        print(f"Image does not exist, will proceed to upload. Error: {str(e)}")

    try:
        # Read the image file
        with open(image_path, 'rb') as file:
            # Upload the image to the specified storage bucket
            upload_response = supabase.storage.from_(storage_bucket).upload(image_name, file)

        # Check if the upload was successful
        if upload_response:  # Check if the upload response is not None or empty
            print(f"Image uploaded successfully: {image_name}")
            return image_name  # Return the uploaded image name (ID)
        else:
            print("Failed to upload image: No response received.")
            return ""  # Return an empty string if the upload fails

    except Exception as e:
        print(f"An error occurred while uploading the image: {str(e)}")
        return ""  # Return an empty string if the upload fails



# ✅ Add Product Function
def add_product(name: str, category: str, price: float, image_path: str = None):
    try:
        # Use timezone-aware UTC datetime and convert to ISO 8601 string
        now_utc = datetime.now(timezone.utc).isoformat()

        # Handle image upload if provided
        image_id = None
        if image_path:
            image_id = upload_image(image_path, 'product-images')  # Replace with your storage bucket name

        # Create a product instance using Pydantic for validation
        product = Product(
            name=name,
            category=category,
            price=price,
            image_id=image_id if image_id else "",  # Ensure image_id is a string
            created_at=now_utc,
            updated_at=now_utc,
        )

        # Insert product into the 'products' table
        data, count = supabase.table("products").insert(product.model_dump()).execute()

        # Check if rows were inserted
        if count:
            print("Product added successfully!")
            print(data)  # Print inserted product details
        else:
            print("Error: No rows were inserted.")

    except ValidationError as e:
        print("Validation Error:", e.json())  # Print validation errors from Pydantic
    except Exception as e:
        print(f"An error occurred: {str(e)}")



# ✅ Example Usage
if __name__ == "__main__":
    add_product(
        name="Apple Juice",
        category="Beverages",
        price=2.99,
        image_path="header-1.jpg"  # Provide the path to the image file
    )
