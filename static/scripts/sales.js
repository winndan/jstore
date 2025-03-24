document.addEventListener("DOMContentLoaded", function () {
    function loadProducts(category = "") {
        fetch(`/api/products?category=${category}`)
            .then(response => response.json())
            .then(products => {
                let productsGrid = document.querySelector(".products-grid");
                productsGrid.innerHTML = "";

                if (products.length === 0) {
                    productsGrid.innerHTML = "<p>No products found.</p>";
                    return;
                }

                products.forEach(product => {
                    let productCard = document.createElement("div");
                    productCard.classList.add("product-card");
                    productCard.innerHTML = `
                        <div class="product-image-container">
                            <img src="${product.image_id}" alt="${product.name}" class="product-image">
                        </div>
                        <div class="product-info">
                            <div class="product-details">
                                <h3 class="product-title">${product.name}</h3>
                                <p class="price">$${product.price}</p>
                            </div>
                            <div class="product-actions">
                                <button class="buy-button" data-id="${product.id}">Buy</button>
                                <button class="restock-button" data-id="${product.id}">Restock</button>
                            </div>
                        </div>
                    `;
                    productsGrid.appendChild(productCard);
                });
            })
            .catch(error => {
                console.error("Error loading products:", error);
                document.querySelector(".products-grid").innerHTML = "<p>Failed to load products. Try again later.</p>";
            });
    }

    // ✅ Load products when clicking category tabs
    document.querySelectorAll(".tab").forEach(tab => {
        tab.addEventListener("click", function () {
            let category = this.getAttribute("data-category");
            loadProducts(category);
        });
    });

    // ✅ Auto-load first category
    let firstCategory = document.querySelector(".tab");
    if (firstCategory) {
        loadProducts(firstCategory.getAttribute("data-category"));
    }

    // ✅ Event Delegation for Restock and Buy buttons
    document.querySelector(".products-grid").addEventListener("click", function (event) {
        if (event.target.classList.contains("restock-button")) {
            let productId = event.target.getAttribute("data-id");
            console.log(`Restocking product with ID: ${productId}`);
            // Add restock functionality here
        }

        if (event.target.classList.contains("buy-button")) {
            let productId = event.target.getAttribute("data-id");
            console.log(`Buying product with ID: ${productId}`);
            // Add buy functionality here
        }
    });
});
