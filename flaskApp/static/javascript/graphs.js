var WeeklyGraphData;
var HourlyGraphData;
var ID;

function getGraphData(){

       //get weekly data for bike stations using fetch
       fetch('http://127.0.0.1:5000/WeeklyGraph',{
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
           WeeklyGraphData = obj.available;



           });


       //get weekly data for bike stations using fetch
       fetch('http://127.0.0.1:5000/HourlyGraph',{
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
           HourlyGraphData = obj.available;

           });

        // call the function every minute to update the information
        setInterval(getGraphData,60000);
}








//test graph!
function updateGraphs(stationID){
    ID = stationID;

    // Load the Visualization API and the piechart package.
    google.charts.load("current", {"packages":["corechart"]});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);

    function drawChart(){
        // // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable();

        data.addColumn('string', 'Weekday');
        data.addColumn('number', 'Available_Bikes');
        data.addColumn('number', 'Available_Spaces');

        for (var i=0;i<WeeklyGraphData.length;i++){
            if(WeeklyGraphData[i].Stop_Number == ID) {
                data.addRows([
                    [
                    WeeklyGraphData[i].Weekday,
                    parseFloat(WeeklyGraphData[i].Available_Bikes),
                    parseFloat(WeeklyGraphData[i].Available_Spaces)
                    ]
                ]);
            }
        }

        var options = {
          title: 'Station ID: ' + stationID.toString(),
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        console.log(data);


        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.LineChart(document.getElementById("weeklyStation"));

        chart.draw(data, options);
    }

}
