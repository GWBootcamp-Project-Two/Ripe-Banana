d3.json("/api/view/VW_ServiceByPopularity").then((data) => { 
    d3.select('#selDataset').append('option').attr('value', '').text(' -- Select A Service -- ')
    data.forEach(element => {
        d3.select('#selDataset').append('option').attr( 'value', element.Service_ID).text(element.Service_Name)
    })
})

getServiceData()
function getServiceData() {
    d3.json("/api/view/streamingservices").then((data) => {

     
        var Service_ID = d3.select('#selDataset').property('value');
        if(Service_ID == '') {
            Service_ID = 34;
        } 

        let service = data.find(service => service.Service_ID == Service_ID)
        // console.log(service)

        d3.select('.panel-body').html('')
        Object.entries(service).forEach(([key, val]) => {
        
            if(key == 'Service_Img'){
                d3.select('.panel-body').append('img').attr('src', val).attr('class', 'Service_Img');
            }else if(key =='Service_URL')   {  
                d3.select('.panel-body').append('a').attr('href', 'http://www.' + val).attr('target', '_blank').text(val);
            }
            else{
                d3.select('.panel-body').append('h6').text(`${key.toUpperCase()}: ${val}`)
            } 
        })
        showData(service)
    })
}
//

function showData(service) {

    var gaugeData = [
        {
            // domain: {x: [0, 1], y: [0, 1]},
            value: service.RipeRating,
            title: { text: "Ripe Rating " + service.Service_Name },
            type: "indicator",
            mode: "gauge+number+delta",
          
            gauge: {
                axis: { range: [null, 10] },
                steps: [
                    { range: [0, 1], color: "rgb(245, 249, 250)" },
                    { range: [1, 2], color: "rgb(225, 233, 235)" },
                    { range: [2, 3], color: "rgb(202, 216, 219)" },
                    { range: [3, 4], color: "rgb(184, 207, 212)" },
                    { range: [4, 5], color: "rgb(174, 203, 209)" },
                    { range: [5, 6], color: "rgb(163, 203, 212)" },
                    { range: [6, 7], color: "rgb(154, 207, 219)" },
                    { range: [7, 8], color: "rgb(154, 214, 227)" },
                    { range: [8, 9], color: "rgb(146, 217, 232)" },
                    { range: [9, 10], color: "rgb(142, 227, 245)" }
                ]
            }
            // delta: {reference: 400},

        }]

    var layout = { width: 600, height: 400 }
    Plotly.newPlot('gauge', gaugeData, layout)
}
function optionChanged() {
    getServiceData();
}
