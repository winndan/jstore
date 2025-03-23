document.addEventListener("DOMContentLoaded", function () {
    fetchInventoryData();
});

async function fetchInventoryData() {
    const response = await fetch("/api/inventory");
    const data = await response.json();
    
    let inventoryDataContainer = document.getElementById("inventory-data");
    inventoryDataContainer.innerHTML = "";
    
    data.forEach(item => {
        inventoryDataContainer.innerHTML += `
            <p>${item.name} - Stock: ${item.stock}</p>
        `;
    });
}
