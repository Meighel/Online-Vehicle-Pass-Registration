// Chart.js Setup
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("trendChart");
    if (!canvas) {
        console.error("Canvas element #trendChart not found!");
        return;
    }

    const ctx = canvas.getContext("2d");

    const chartData = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [
            {
                label: "Paid Clients",
                data: [10, 15, 13, 20, 25, 22, 30, 28, 35, 40, 45, 50], // Sample Data
                borderColor: "#ffcc00",
                backgroundColor: "rgba(255, 204, 0, 0.2)",
                borderWidth: 2,
                fill: true,
                tension: 0.4,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
            },
            y: {
                beginAtZero: true,
            },
        },
    };

    new Chart(ctx, {
        type: "line",
        data: chartData,
        options: chartOptions,
    });

    console.log("Chart initialized successfully.");
});