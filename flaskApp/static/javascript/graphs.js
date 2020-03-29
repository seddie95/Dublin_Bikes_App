var graphData;


function getGraphData(){

       //get static data for bike stations using fetch
       fetch('http://127.0.0.1:5000/graph',{
            method: "POST",
            credentials: "include",
            body: JSON.stringify(""),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
       }).then(function (response) {
               return response.json();
               // use the static data to create dictionary
           }).then(function (obj) {
           graphData = obj.available;

           console.log(graphData);


           });

        // call the function every minute to update the information
        setInterval(getGraphData,60000);
}



//test graph!
function updateGraphs(stationID){
    // console.log(staticData);


    // Load the Visualization API and the piechart package.
    google.charts.load("current", {"packages":["corechart"]});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);

    function drawChart(){
        // // Create our data table out of JSON data loaded from server.
        // var data = new google.visualization.DataTable(staticData);

        var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses'],
          ['2004',  1000,      400],
          ['2005',  1170,      460],
          ['2006',  660,       1120],
          ['2007',  1030,      540]
        ]);

        var options = {
          title: 'Station ID: ' + stationID.toString(),
          curveType: 'function',
          legend: { position: 'bottom' }
        };



        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.LineChart(document.getElementById("weeklyStation"));

        chart.draw(data, options);
    }

}
