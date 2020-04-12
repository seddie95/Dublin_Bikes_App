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
        setTimeout(getGraphData,60000);
}


function updateGraphs(stationID){
    ID = stationID;

    // Load the Visualization API and the corechart package.
    google.charts.load("current", {"packages":["corechart"]});

    // Weekly Chart
    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawWeeklyChart);

    function drawWeeklyChart(){
        // // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable();

        data.addColumn('string', 'Weekday');
        data.addColumn('number', 'Available Bikes');
        data.addColumn('number', 'Available Spaces');

        for (var i=0;i<WeeklyGraphData.length;i++){
            if(WeeklyGraphData[i].Stop_Number == ID) {
                data.addRows([
                    [
                    WeeklyGraphData[i].Weekday.substring(0,3),
                    Math.round(parseFloat(WeeklyGraphData[i].Available_Bikes)),
                    Math.round(parseFloat(WeeklyGraphData[i].Available_Spaces))
                    ]
                ]);
            }
        }

        var options = {
            title: 'Average daily availability at this station',
            titleTextStyle: {
                color: '#2f2f2f',
                fontSize: 14
            },
            width: 500,
            height: 200,
            curveType: 'function',
            legend: { position: 'bottom' },
            fontName: 'Open Sans',
            hAxis: {
                slantedText: false,
                showTextEvery: 1,
            },
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.LineChart(document.getElementById("weeklyStation"));

        chart.draw(data, options);
    }


    // Hourly Chart
    // Load the Visualization API and the corechart package.
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
                'filterColumnLabel': 'Hours',
                'ui': {
                    'label': "",
                    'format': {
                        'fractionDigits': 0,
                        'suffix': ":00",
                    },
                },
                // Remove if not needed later
      //          'ui.cssClass': 	'google-visualization-controls-rangefilter',
            },
            'state': {'lowValue': 0, 'highValue': 23}
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
                    'sortValues' : false,
                    'label': "",
      //              'cssClass': 'google-visualization-controls-categoryfilter',
                }
            },
        });

        var chart  = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'chart_div',
            'options': {
                'title': 'Average hourly availability at this station',
                'titleTextStyle': {
                    'color': '#2f2f2f',
                    'fontSize': 14
                    },
                'width': 500,
                'height': 200,
                'legend': 'bottom',
                'fontName': 'Open Sans',
                'hAxis': {
                    'ticks': [{v:0, f:'0:00'},{v:5, f:'05:00'}, {v:10, f:'10:00'}, {v:15, f:'15:00'}, {v:20, f:'20:00'}],
                    },
                },
            'view': {'columns': [1,2,3]},
        });

        // // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable();

        data.addColumn('string', 'Weekday');
        data.addColumn('number', 'Hours');
        data.addColumn('number', 'Available Bikes');
        data.addColumn('number', 'Available Spaces');

        for (var i=0;i<HourlyGraphData.length;i++){
            if(HourlyGraphData[i].Stop_Number == ID) {
                data.addRows([
                    [
                    HourlyGraphData[i].Weekday,
                    parseInt(HourlyGraphData[i].Hours),
                    Math.round(parseFloat(HourlyGraphData[i].AvgBike)),
                    Math.round(parseFloat(HourlyGraphData[i].AvgSpace))
                    ]
                ]);
            }
        }

        var formatter = new google.visualization.NumberFormat({suffix: ':00', fractionDigits: 0});
        formatter.format(data, 1); // Apply formatter to second column

        dashboard.bind([slider,filter], chart);
        dashboard.draw(data);
    }

}
