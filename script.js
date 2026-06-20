// Weather Analysis Chart
new Chart(document.getElementById("weatherChart"), {
    type: "bar",
    data: {
        labels: ["Sunny", "Rain", "Fog", "Snow"],
        datasets: [{
            label: "Accidents",
            data: [8000, 12000, 3500, 1500]
        }]
    }
});

// Road Type Chart
new Chart(document.getElementById("roadChart"), {
    type: "pie",
    data: {
        labels: ["Highway", "City Road", "Village Road", "Expressway"],
        datasets: [{
            data: [35, 30, 20, 15]
        }]
    }
});

// Hour-wise Chart
new Chart(document.getElementById("hourChart"), {
    type: "line",
    data: {
        labels: ["6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"],
        datasets: [{
            label: "Accidents",
            data: [20, 45, 35, 50, 80, 40]
        }]
    }
});

// Severity Chart
new Chart(document.getElementById("severityChart"), {
    type: "doughnut",
    data: {
        labels: ["Low", "Medium", "High"],
        datasets: [{
            data: [40, 35, 25]
        }]
    }
});

// Top Cities Chart
new Chart(document.getElementById("cityChart"), {
    type: "bar",
    data: {
        labels: ["Hyderabad", "Visakhapatnam", "Vijayawada", "Guntur", "Warangal"],
        datasets: [{
            label: "Accidents",
            data: [520, 430, 380, 300, 250]
        }]
    }
});