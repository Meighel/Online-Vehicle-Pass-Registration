// Get the canvas element
var ctx = document.getElementById('registrationChart').getContext('2d');
    
// Chart data
var data = {
    labels: ["Pending Applicants", "Rejected", "Approved"],
    datasets: [{
    data: [550, 185, 120], // Change values as needed
    backgroundColor: ["#007bff", "#dc3545", "#28a745"], // Blue, Red, Green
    hoverOffset: 10
            }]
        };
    
        // Create Doughnut Chart
        var registrationChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ["Applicants", "Rejected", "Approved"],
                datasets: [{
                    data: [550, 185, 120],
                    backgroundColor: ["#007bff", "#dc3545", "#28a745"],
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: 5
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Registration Overview', // Your chart title
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        color: '#000',
                        padding: {
                            top: 10,
                            bottom: 10
                        }
                    }
                }
            }
        });



// PAYMENT