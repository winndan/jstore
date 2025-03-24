document.addEventListener("DOMContentLoaded", function () {
    async function loadProducts(category = "") {
        try {
            let response = await fetch(`/api/products?category=${category}`);
            if (!response.ok) throw new Error("Failed to fetch products");

            let products = await response.json();
            let productsGrid = document.querySelector(".products-grid");
            productsGrid.innerHTML = "";

            if (products.length === 0) {
                productsGrid.innerHTML = "<p>No products found.</p>";
                return;
            }

            products.forEach(product => {
                let priceValue = parseFloat(product.price.replace(/[^0-9.]/g, ""));
                let price = `₱${priceValue.toLocaleString("en-PH", { minimumFractionDigits: 2 })}`;

                let productCard = document.createElement("div");
                productCard.classList.add("product-card");
                productCard.innerHTML = `
                    <div class="product-image-container">
                        <img src="${product.image_id}" alt="${product.name}" class="product-image">
                    </div>
                    <div class="product-info">
                        <div class="product-details">
                            <h3 class="product-title">${product.name}</h3>
                            <p class="price">${price}</p>
                        </div>
                        <button class="add-button">Add to Cart</button>
                    </div>
                `;

                productsGrid.appendChild(productCard);
            });
        } catch (error) {
            console.error("Error loading products:", error);
            document.querySelector(".products-grid").innerHTML = "<p>Failed to load products. Try again later.</p>";
        }
    }

    document.querySelectorAll(".tab").forEach(tab => {
        tab.addEventListener("click", function () {
            let category = this.getAttribute("data-category");
            loadProducts(category);
            document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
            this.classList.add("active");
        });
    });

    let firstCategory = document.querySelector(".tab");
    if (firstCategory) {
        firstCategory.classList.add("active");
        loadProducts(firstCategory.getAttribute("data-category"));
    }
});
