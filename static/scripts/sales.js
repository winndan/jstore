document.addEventListener("DOMContentLoaded", function () {
    fetchSalesData();

    // Attach click event to category buttons
    document.querySelectorAll(".tab").forEach(button => {
        button.addEventListener("click", function () {
            const category = this.getAttribute("data-category");
            document.querySelectorAll(".tab").forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
            fetchSalesData(category);
        });
    });

    // Search functionality
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase();
            filterSales(query);
        });
    }
});

async function fetchSalesData(category = "") {
    try {
        const response = await fetch(`/api/sales?category=${category}`);
        if (!response.ok) throw new Error("Failed to fetch sales data");
        const data = await response.json();
        
        let salesDataContainer = document.getElementById("sales-data");
        if (!salesDataContainer) return;
        salesDataContainer.innerHTML = "";  // Clear existing content

        if (data.length === 0) {
            salesDataContainer.innerHTML = "<p class='no-sales'>No sales found.</p>";
            return;
        }

        data.forEach(sale => {
            salesDataContainer.innerHTML += `
                <div class="sale-item">
                    <p><strong>${sale.customer}</strong> - ₱${sale.total}</p>
                    <small>${sale.date}</small>
                </div>
            `;
        });

        updateOrderSummary();
    } catch (error) {
        console.error("Error fetching sales data:", error);
        let salesDataContainer = document.getElementById("sales-data");
        if (salesDataContainer) {
            salesDataContainer.innerHTML = "<p class='error-message'>Error loading sales data.</p>";
        }
    }
}

function filterSales(query) {
    document.querySelectorAll(".sale-item").forEach(item => {
        item.style.display = item.innerText.toLowerCase().includes(query) ? "block" : "none";
    });
}

function updateOrderSummary() {
    let orderSummary = document.getElementById("order-summary");
    if (orderSummary) {
        orderSummary.innerHTML = `
            <p>Subtotal: ₱0.00</p>
            <p>Discount: ₱0.00</p>
            <p>Tax: ₱0.00</p>
            <p><strong>Total: ₱0.00</strong></p>
        `;
    }
}
