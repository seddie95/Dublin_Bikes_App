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
           })

       // catch used to test if something went wrong when parsing or in the network
       .catch(function (error) {
           console.error("Difficulty fetching data for weekly graph:", error);
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
           })

          // catch used to test if something went wrong when parsing or in the network
       .catch(function (error) {
           console.error("Difficulty fetching data for hourly graph:", error);
       });


        // call the function every minute to update the information
        // setTimeout(getGraphData,60000);
}





function updateGraphs(stationID){
    ID = stationID;

    // Load the Visualization API and the piechart package.
    google.charts.load("current", {"packages":["corechart"]});

    // Weekly Chart
    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawWeeklyChart);

    function drawWeeklyChart(){
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
            width: 500,
            height: 200,
            curveType: 'function',
            legend: { position: 'bottom' }
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.LineChart(document.getElementById("weeklyStation"));

        chart.draw(data, options);
    }


    //hourly Chart
    // Load the Visualization API and the piechart package.
    google.charts.load('current', {'packages':['corechart', 'controls']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawHourlyChart);

    function drawHourlyChart(){
        // create dashboard for the graph and controls
        var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

        // create a slider
        var slider = new google.visualization.ControlWrapper({
            'controlType': 'NumberRangeFilter',
            'containerId': 'slider_div',
            'options': {
                'filterColumnLabel': 'Hours'
            },
            'state': {'lowValue': 0, 'highValue': 24}
        });

        // create a filter
        var filter = new google.visualization.ControlWrapper({
            'controlType': 'CategoryFilter',
            'containerId': 'filter_div',
            'options': {
                'filterColumnLabel': 'Weekday',
                'ui': {
                    'allowMultiple' : false,
                    'allowNone' : false,
                    'selectedValuesLayout' : 'below',
                    'sortValues' : false
                }
            },
        });

        var chart  = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'chart_div',
            'options': {
                'title': 'Station ID: ' + stationID.toString(),
                'width': 500,
                'height': 200,
                'legend': 'bottom',
            },
            'view': {'columns': [1,2,3]}
        });

        // // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable();

        data.addColumn('string', 'Weekday');
        data.addColumn('number', 'Hours');
        data.addColumn('number', 'Available_Bikes');
        data.addColumn('number', 'Available_Spaces');

        for (var i=0;i<HourlyGraphData.length;i++){
            if(HourlyGraphData[i].Stop_Number == ID) {
                data.addRows([
                    [
                    HourlyGraphData[i].Weekday,
                    parseInt(HourlyGraphData[i].Hours),
                    parseFloat(HourlyGraphData[i].AvgBike),
                    parseFloat(HourlyGraphData[i].AvgSpace)
                    ]
                ]);
            }
        }


        dashboard.bind([slider,filter], chart);
        dashboard.draw(data);
    }

}
