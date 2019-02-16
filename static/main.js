$.getJSON('http://localhost:5000/data/json', function(data) {
console.log(data);
var femme = data.prostitues.Calvados.femmes;
var homme = data.prostitues.Calvados.hommes;
var trans = data.prostitues.Calvados.trans;
var ctx = document.getElementById("myChart");
// var test = document.getElementsByTagName('p')[0].innerHTML;
        var myChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: ["Femme", "Homme", "Trans"],
                datasets: [{
                    label: '# of Votes',
                    data: [femme, homme, trans],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
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