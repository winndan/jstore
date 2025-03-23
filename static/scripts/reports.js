document.addEventListener("DOMContentLoaded", function () {
    fetchReportData();
});

async function fetchReportData() {
    const response = await fetch("/api/reports");
    const data = await response.json();
    
    let reportDataContainer = document.getElementById("report-data");
    reportDataContainer.innerHTML = "";
    
    data.forEach(report => {
        reportDataContainer.innerHTML += `
            <p>${report.date} - Total Sales: ₱${report.total}</p>
        `;
    });
}
