document.addEventListener("DOMContentLoaded", function () {
    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach(item => {
        item.addEventListener("click", function () {
            let page = this.getAttribute("data-page");
            loadPage(page);

            // Remove active class from all items and set to clicked item
            navItems.forEach(nav => nav.classList.remove("active"));
            this.classList.add("active");
        });
    });
});

function loadPage(page) {
    let mainContent = document.querySelector(".main-content");

    switch (page) {
        case "sales":
            mainContent.innerHTML = `
                <h1>Sales Tracking</h1>
                <p>Track customer purchases and sales transactions here.</p>
            `;
            break;

        case "add-products":
            mainContent.innerHTML = `
                <h1>Add New Product</h1>
                <form id="product-form">
                    <input type="text" id="product-name" placeholder="Product Name" required>
                    <input type="number" id="product-price" placeholder="Price" required>
                    <input type="number" id="product-stock" placeholder="Stock" required>
                    <button type="submit">Add Product</button>
                </form>
            `;
            break;

        case "credit":
            mainContent.innerHTML = `
                <h1>Customer Credit</h1>
                <p>Manage customer debts and credits here.</p>
            `;
            break;

        case "reports":
            mainContent.innerHTML = `
                <h1>Reports & Bookkeeping</h1>
                <p>View sales reports and financial records here.</p>
            `;
            break;

        case "inventory":
            mainContent.innerHTML = `
                <h1>Inventory Management</h1>
                <p>Monitor and update stock levels here.</p>
            `;
            break;

        default:
            mainContent.innerHTML = "<h1>Welcome to the POS System</h1>";
            break;
    }
}
