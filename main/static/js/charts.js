document.addEventListener("DOMContentLoaded", function () {

    const dataDiv = document.getElementById("chart-data");

    if (!dataDiv) return;

    const labels = JSON.parse(dataDiv.dataset.labels);
    const values = JSON.parse(dataDiv.dataset.values);
    const income = Number(dataDiv.dataset.income);
    const expenses = Number(dataDiv.dataset.expenses);

    // Pie Chart 
    const pieCtx = document.getElementById("categoryChart");

    if (pieCtx) {
        new Chart(pieCtx, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values
                }]
            }
        });
    }

    // Bar Chart
    const barCtx = document.getElementById("barChart");

    if (barCtx) {
        new Chart(barCtx, {
            type: "bar",
            data: {
                labels: ["Income", "Expenses"],
                datasets: [{
                    label: "Amount",
                    data: [income, expenses]
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
