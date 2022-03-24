function getchart(label,dataset){
    var ctx = document.getElementById('myChart');
    var ctx2 = document.getElementById('myChart2');
    var ctx3 = document.getElementById('myChart3');
    if (ctx!=null){
        var myChart= new Chart(ctx, {
            type: 'pie',
            data: {
                labels: label,
                datasets: [{
                    label: 'Last year income details ',
                    data: dataset,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                title:{
                    display:true,
                    text:"Last year income summary"
                },
                responsive: true
            }
        
        });
    }
    if(ctx3!=null){
        var myChart3 = new Chart(ctx3, {
            type: 'line',
            data: {
                labels: label,
                datasets: [{
                    label: 'Last year income details ',
                    data: dataset,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                title:{
                    display:true,
                    text:"Last year income summary"
                },
                responsive: true,
            }
        });
    }
    if(ctx2!=null) {
    var myChart2 = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: label,
            datasets: [{
                label: 'Last year income details ',
                data: dataset,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title:{
                display:true,
                text:"Last year income summary"
            },
            responsive: true,
            
        }
    });
    }
   
}
function fetchdata(){
    fetch('/income/statapi/',{
        method: "GET"})
        .then((res)=>res.json()).then((data)=>{
            console.log(data);
            const res=data.inc_result;
            const [labels,dataset]=[
                Object.keys(res),
                Object.values(res),
            ];
            // console.log(labels,dataset);
            getchart(labels,dataset);
        })
}
document.onload=fetchdata();
