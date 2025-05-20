document.addEventListener("DOMContentLoaded", () => {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    // Chart 2: Paid Clients
    const paidCanvas = document.getElementById("paidChart");
    if (paidCanvas) {
        new Chart(paidCanvas.getContext("2d"), {
            type: "bar",
            data: {
                labels: months,
                datasets: [{
                    label: "Paid Clients",
                    data: paidClientsData,
                    backgroundColor: "rgba(255, 206, 86, 0.5)",
                    borderColor: "#ffcc00",
                    borderWidth: 1,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: true }},
                scales: { y: { beginAtZero: true }},
            },
        });
    }
});
