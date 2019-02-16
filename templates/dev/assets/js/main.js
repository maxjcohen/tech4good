$.getJSON("./data/data.json", function(data) {
    var sum = 0;
    var totals = [];
    var names = [];
    var index;

    for ( index = 0; index < Object.keys(data.actions).length; index++) {
        names.push(Object.keys(data.actions)[index]);
    }

    for (var y = 0; y < names.length; y++) {
        for ( i = 0; i < Object.keys(data.actions)[y].length; i++) {
            var val = Object.values(data.actions)[y];
        }
        for (var b = 0; b < Object.values(val).length; b++) {
            var test = Object.values(val)[b];
            sum +=Object.values(test)[0];
        }
        totals.push(sum);
        sum = 0;
    }

var lineChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
        label: 'My First dataset',
        borderColor: window.chartColors.red,
        backgroundColor: window.chartColors.red,
        fill: false,
        data: [
            8,
            55,
            60,
            3,
            33,
            67,
            90
        ],
        yAxisID: 'y-axis-1',
    }, {
        label: 'My Second dataset',
        borderColor: window.chartColors.blue,
        backgroundColor: window.chartColors.blue,
        fill: false,
        data: [
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor(),
            randomScalingFactor()
        ],
        yAxisID: 'y-axis-2'
    }]
};

window.onload = function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    window.myLine = Chart.Line(ctx, {
        data: lineChartData,
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: true,
                text: 'Chart.js Line Chart - Multi Axis'
            },
            scales: {
                yAxes: [{
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                }, {
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'right',
                    id: 'y-axis-2',

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            }
        }
    });
};

var ctx = document.getElementById("myChart2");
var test = document.getElementsByTagName('p')[0].innerHTML;
    var myChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: [names[0], names[1], names[2], names[3], names[4]],
            datasets: [{
                label: '# of Votes',
                data: [totals[0], totals[1], totals[2], totals[3], totals[4]],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
});