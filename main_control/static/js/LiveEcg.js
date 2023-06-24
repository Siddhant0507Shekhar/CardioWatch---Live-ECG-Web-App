// Get the canvas element from HTML
var ctx = document.getElementById('myChart').getContext('2d');

// Create an initial empty chart
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Live Data',
            data: [],
            pointRadius: 0, // Set point radius
            // pointColors: 'rgb(0,0,255)',
            // pointBackgroundColor: 'blue',
            borderWidth: 2,
            borderColor: 'rgb(0, 0,255)',
            fill: false
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'linear',
                ticks: {
                    // max: 20,
                    // min: 0,
                    stepSize: 1,
                    callback: function (value, index, values) {
                        return value + ' s';
                    }
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Time'
                }
            }],
            yAxes: [{
                ticks: {
                    suggestedMax: 4500,
                    suggestedMin: 1300,
                    steps: 100,
                    stepValue: 5,
                    // min: 300,
                    // max:1500
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Data'
                }
            }]
        }
    }
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// function sleep(delay) {
//   var start = new Date().getTime();
//   while (new Date().getTime() < start + delay);
// }


function updateChart() {
    // Make an API call to get the data
    fetch('/api/get_live_data')
        .then(response => response.json())
        .then(function (data) {
            while (myChart.data.labels.length > 0) {
                    myChart.data.labels.shift();
                    myChart.data.datasets[0].data.shift();
                }
            myChart.update();
            // Add new data to the chart
            var ecg_arr = data.live_arr;
            console.log(ecg_arr);
            let live_arr = ecg_arr.replace(/[\[\]]/g, "").split(" ").filter(Boolean).map(x => parseInt(x));
            // for (var d = 0; d < live_arr.length; d++) {
            //     if (live_arr[d] < 1500) {
            //         live_arr[d] = 1500;
            //     }
            // }

            var currentTime = new Date().getTime();
            for (var i = 0; i < live_arr.length; i++) {
                myChart.data.labels.push(currentTime);
                myChart.data.datasets[0].data.push(live_arr[i]);
                currentTime += 30; // increment by 30 milisecond
                // Remove data older than 20 seconds
                var timeLimit = currentTime - 18000;
                // sleep(20)
                while (myChart.data.labels[0] < timeLimit) {
                    myChart.data.labels.shift();
                    myChart.data.datasets[0].data.shift();
                    myChart.update();
                }
                // await sleep(25);

                // Update the chart
                myChart.update();
            }
        });
}

// updateChart();
// Call updateChart function every 20 seconds
setInterval(updateChart, 20000);
