document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const day = document.getElementById('day').value;
    const speed = document.getElementById('speed').value;
    const distance = document.getElementById('distance').value;
    const time = document.getElementById('time').value;

    fetch('/add_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ day, speed, distance, time }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Data added successfully!');
        fetchData();
    });
});

document.getElementById('timeRange').addEventListener('input', function() {
    const timeRange = this.value;
    let range;
    if (timeRange == 1) range = 'day';
    else if (timeRange == 2) range = 'month';
    else if (timeRange == 3) range = 'year';

    fetch(`/plot?time_range=${range}`)
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        document.getElementById('usageChart').src = url;
    });
});

function fetchData() {
    fetch('/get_data')
    .then(response => response.json())
    .then(data => {
        renderStats(data);
        setAverages(data);
    });

    fetch('/plot?time_range=day')
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        document.getElementById('usageChart').src = url;
    });
}

function renderStats(data) {
    const statsDiv = document.getElementById('stats');
    const distances = data.map(item => item[3]);
    const total = distances.reduce((a, b) => a + b, 0);
    const max = Math.max(...distances);
    const min = Math.min(...distances);
    const avg = total / distances.length;

    statsDiv.innerHTML = `
        <p>Total Distance: ${total.toFixed(2)} km</p>
        <p>Max Distance: ${max.toFixed(2)} km</p>
        <p>Min Distance: ${min.toFixed(2)} km</p>
        <p>Avg Distance: ${avg.toFixed(2)} km</p>
    `;
}

function setAverages(data) {
    const speeds = data.map(item => item[2]);
    const distances = data.map(item => item[3]);
    const times = data.map(item => item[4]);

    const avgSpeed = speeds.length > 0 ? speeds.reduce((a, b) => a + b, 0) / speeds.length : 0;
    const avgDistance = distances.length > 0 ? distances.reduce((a, b) => a + b, 0) / distances.length : 0;
    const avgTime = times.length > 0 ? times.reduce((a, b) => a + b, 0) / times.length : 0;

    document.getElementById('speed').placeholder = `Avg Speed: ${avgSpeed.toFixed(2)} km/h`;
    document.getElementById('distance').placeholder = `Avg Distance: ${avgDistance.toFixed(2)} km`;
    document.getElementById('time').placeholder = `Avg Time: ${avgTime.toFixed(2)} min`;
}

fetchData();

function setNightOrLight() {
    if (document.getElementById('nightOrLight').innerText == "🌚") {
        document.getElementById('nightOrLight').innerText = "🌝"
        document.body.style.backgroundColor = "#002B36";
        document.body.style.color = "#E3F7FC";
    } else {
        document.getElementById('nightOrLight').innerText = "🌚"
        document.body.style.backgroundColor = "#FDF6E3";
        document.body.style.color = "#362700";
    }
}