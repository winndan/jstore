document.addEventListener("DOMContentLoaded", function () {
    setupNavigation();
    loadPage("home"); // Load home page by default
});

// ✅ Handle Sidebar Navigation (UI Only)
function setupNavigation() {
    document.querySelectorAll(".nav-item").forEach((item) => {
        item.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent unwanted behavior

            document.querySelectorAll(".nav-item").forEach((el) => el.classList.remove("active"));
            this.classList.add("active");

            let page = this.getAttribute("data-page");
            loadPage(page);
        });
    });
}

// ✅ Load Page Content Dynamically
function loadPage(page) {
    let content = document.getElementById("main-content");
    if (!content) {
        console.error("Main content container not found!");
        return;
    }
    content.innerHTML = getPageContent(page);
}

// ✅ Page Content Definitions (Frontend Only)
function getPageContent(page) {
    switch (page) {
        case "home":
            return `<h1>🏠 Home</h1><p>Welcome to FreshMart POS. Select a category from the sidebar.</p>`;
        case "sales":
            return `<h1>📈 Sales Dashboard</h1><p>View and manage sales transactions here.</p>`;
        case "add-products":
            return `<h1>🛒 Add New Products</h1><p>Manage inventory and add new products.</p>`;
        case "credit":
            return `<h1>💳 Customer Credit</h1><p>Track customer credit and pending payments.</p>`;
        case "reports":
            return `<h1>📊 Reports & Analytics</h1><p>View sales and business performance reports.</p>`;
        case "inventory":
            return `<h1>📦 Inventory Management</h1><p>Track product stock and manage supplies.</p>`;
        case "customers":
            return `<h1>🧑‍🤝‍🧑 Customer Management</h1><p>View and manage customer details.</p>`;
        default:
            return `<h1>⚠ Page Not Found</h1>`;
    }
}
