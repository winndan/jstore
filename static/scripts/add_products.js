document.addEventListener("DOMContentLoaded", function () {
    fetchProducts();

    // ✅ Handle search filtering
    document.getElementById("search-input")?.addEventListener("input", function () {
        const query = this.value.toLowerCase();
        document.querySelectorAll(".product-card").forEach(item => {
            const name = item.querySelector(".product-name").innerText.toLowerCase();
            const category = item.querySelector(".product-category").innerText.toLowerCase();
            const price = item.querySelector(".product-price").innerText.toLowerCase();
            
            item.style.display = (name.includes(query) || category.includes(query) || price.includes(query)) ? "block" : "none";
        });
    });
});

// ✅ Fetch all products from Supabase
async function fetchProducts() {
    try {
        const response = await fetch("/api/products");
        if (!response.ok) throw new Error("Failed to fetch products");

        const data = await response.json();
        let productList = document.getElementById("product-list");
        productList.innerHTML = "";

        if (!data.length) {
            productList.innerHTML = "<p class='no-products'>No products found.</p>";
            return;
        }

        const fragment = document.createDocumentFragment(); // Optimized rendering

        data.forEach(product => {
            const productCard = document.createElement("div");
            productCard.classList.add("product-card");

            productCard.innerHTML = `
                <div class="product-image">
                    <img src="${product.image_url}" alt="${product.name}">
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-category"><strong>Category:</strong> ${capitalizeWords(product.category)}</p>
                    <p class="product-price"><strong>Price:</strong> ₱${parseFloat(product.price).toFixed(2)}</p>
                    <p><strong>Stock:</strong> ${product.stock}</p>
                </div>
            `;

            fragment.appendChild(productCard);
        });

        productList.appendChild(fragment);
    } catch (error) {
        console.error("Error fetching products:", error);
        document.getElementById("product-list").innerHTML = `<p class='error-message'>Error loading products. Please try again later.</p>`;
    }
}

// ✅ Function to capitalize the first letter of each word
function capitalizeWords(str) {
    return str.replace(/\b\w/g, char => char.toUpperCase());
}
