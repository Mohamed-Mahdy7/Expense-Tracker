document.addEventListener("DOMContentLoaded", function () {
  const dataDiv = document.getElementById("chart-data");

  if (!dataDiv) return;

  const labels = JSON.parse(dataDiv.dataset.labels);
  // const labels = ['income','expenses']
  // console.log(labels)
  const values = JSON.parse(dataDiv.dataset.values);
  // const values = [100,274]
  const income = Number(dataDiv.dataset.income);
  const expenses = Number(dataDiv.dataset.expenses);
  console.log(values);
  // Pie Chart
  const pieCtx = document.getElementById("pieChart");

  if (pieCtx) {
    new Chart(pieCtx, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
          },
        ],
      },
    });
  }

  // Bar Chart
  const barCtx = document.getElementById("barChart");
  const data = [
    { title: "one", value: 100 },
    { title: "two", value: 200 },
    { title: "three", value: 140 },
    { title: "four", value: 300 },
  ];
  const barChartLabels = data.map((item) => item.title);
  const barChartValue = data.map((item) => item.value);
  if (barCtx) {
    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: barChartLabels,
        datasets: [
          {
            label: "Amount",
            data: barChartValue,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
});
