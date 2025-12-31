document.addEventListener("DOMContentLoaded", function () {
  const dataDiv = document.getElementById("chart-data");
  if (!dataDiv) return;

  // Pie
  const pieLabels = JSON.parse(dataDiv.dataset.pieLabels);
  const pieValues = JSON.parse(dataDiv.dataset.pieValues);

  const pieCtx = document.getElementById("pieChart");
  if (pieCtx) {
    new Chart(pieCtx, {
      type: "pie",
      data: {
        labels: pieLabels,
        datasets: [{ data: pieValues }]
      }
    });
  }

  // Bar
  const barLabels = JSON.parse(dataDiv.dataset.barLabels);
  const barValues = JSON.parse(dataDiv.dataset.barValues);

  const barCtx = document.getElementById("barChart");
  if (barCtx) {
    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: barLabels,
        datasets: [{
          label: "Amount",
          data: barValues
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    });
  }
});
