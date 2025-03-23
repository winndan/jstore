document.addEventListener("DOMContentLoaded", function () {
    fetchProducts();

    // ✅ Handle search filtering
    document.getElementById("search-input")?.addEventListener("input", function () {
        const query = this.value.toLowerCase();
        document.querySelectorAll(".product-card").forEach(item => {
            item.style.display = item.innerText.toLowerCase().includes(query) ? "block" : "none";
        });
    });
});

// ✅ Fetch all products from Supabase
async function fetchProducts() {
    try {
        const response = await fetch("/api/products");
        const data = await response.json();
        let productList = document.getElementById("product-list");
        productList.innerHTML = "";

        if (!data.length) {
            productList.innerHTML = "<p class='no-products'>No products found.</p>";
            return;
        }

        data.forEach(product => {
            const productCard = document.createElement("div");
            productCard.classList.add("product-card");

            productCard.innerHTML = `
                <div class="product-image">
                    <img src="${product.image_url}" alt="${product.name}">
                </div>
                <div class="product-info">
                    <h3>${product.name}</h3>
                    <p><strong>Category:</strong> ${product.category}</p>
                    <p><strong>Price:</strong> ₱${product.price.toFixed(2)}</p>
                    <p><strong>Stock:</strong> ${product.stock}</p>
                </div>
            `;

            productList.appendChild(productCard);
        });
    } catch (error) {
        console.error("Error fetching products:", error);
        document.getElementById("product-list").innerHTML = "<p class='error-message'>Error loading products.</p>";
    }
}
