//Global variables
var markers = [];
var allStations=[];
var availableStands = [];
var availableBikes= [];
var map;


let firstTime = true;

function initMap() {
       //get static data for bike stations using fetch
       fetch('http://127.0.0.1:5000/dynamic')
           .then(function (response) {
               return response.json();
               // use the static data to create dictionary
           }).then(function (obj) {
               staticData = obj.available

               //setting the coordinates for the centre of the  map
               var location = {
                   lat: 53.348071,
                   lng: -6.268233
               };

               // set the zoom level for the first time receiving the data
               if (firstTime){
                    // set the map to be equal to the div with id "map"
                    map = new google.maps.Map(document.getElementById("map"), {
                       zoom: 14,
                       center: location
                    });

                    // create an infowindow
                    var infowindow = new google.maps.InfoWindow();

                    //loop through static data to create markers for the map
                    var marker,i,selectedMarker;
                    for (i = 0; i < staticData.length; i++) {
                        // set the bike icon to blue if  status is open or grey if closed
                        var icon;
                        if (staticData[i].Station_Status == 'OPEN') {
                           icon = "/static//icons/bikeIcon.png";
                        } else {
                           icon = "/static//icons/closedIcon.png";
                        }

                        // set the  of the markers using the longitude and latitude of the station
                        marker = new google.maps.Marker({
                           position: {
                               lat: parseFloat(staticData[i].Pos_Lat),
                               lng: parseFloat(staticData[i].Pos_Lng)
                           },
                           map: map,


                           // give the markers a title of the stop name and number
                           title: staticData[i].Stop_Name,
                           station_number: staticData[i].Stop_Number.toString(),

                           // set the icon of the to the bike icon and scale it
                           icon: {
                               url: icon,
                               scaledSize: new google.maps.Size(40, 40)
                           },
                           // animation: google.maps.Animation.DROP
                        });

                        //add each marker to markers array so they can be referred to individually
                        markers[staticData[i].Stop_Number] = marker;
                        allStations.push(marker);

                        //add the markers with available bikes to the availableBikes array
                        if (staticData[i].Available_Bikes >0){
                            availableBikes.push(marker);
                        }

                        //add the markers with available Stands to the availableStands array
                        if (staticData[i].Available_Spaces >0){
                            availableStands.push(marker);
                        }

                        // add listener to zoom to the location of the marker and display content
                        google.maps.event.addListener(marker, 'click', (function(marker, i) {
                                return function() {
                                    // zoom in on the marker selected
                                    map.setZoom(15);

                                    // center selected marker
                                    map.setCenter(marker.position);

                                    // Change the colour and size of the marker selected and return it to normal when new marker is clicked
                                    if (selectedMarker) {
                                        selectedMarker.setIcon({
                                        url: icon,
                                        scaledSize: new google.maps.Size(40, 40)});
                                    }

                                    marker.setIcon({
                                        url: "/static//icons/selectBike.png",
                                        scaledSize: new google.maps.Size(70, 70)});

                                    selectedMarker = marker;

                                    var date = new Date()
                                    // Set the content of the info window to display the dynamic bike data
                                    infowindow.setContent(
                                                "Last Update: " + date.toUTCString() + "<br>" +
                                                "Stop Name: " + staticData[i].Stop_Name + "<br>" +
                                               "Stop ID: " + staticData[i].Stop_Number.toString() +"<br>" +
                                               "Available Bikes: " + staticData[i].Available_Bikes.toString() +'<br>'+
                                               "Available Spaces: " +staticData[i].Available_Spaces.toString() +'<br>'+
                                               "Banking: " + staticData[i].Banking
                                               );
                                    infowindow.open(map, marker);
                                }
                              })(marker, i));
                    }
                    firstTime= false;
               }
           })
           // catch used to test if something went wrong when parsing or in the network
           .catch(function (error) {
               console.error("Somethings wrong:", error);
               console.error(error);
           });
    // call the function every minute to update the information
    setInterval(initMap,60000)
}



//-----------------------------------------------------------
// Below are the functions to hide the dynamic data depending on available bikes or stands

// shows or hides  all of the markers on the map
function setMapOnAll(map) {
    for (var i = 0; i < allStations.length; i++) {
        allStations[i].setMap(map);
    }
}

// Shows all of the markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}

// Hide stations where there are no available bikes.
function showAvailableBikes() {
    showBikes(map,availableBikes);
}

// Hide stations where there are no available stands.
function showAvailableStands() {
    showBikes(map,availableStands);
}

// shows all of the markers in the selected array while hiding the others not in the array
function showBikes(map,array) {
    setMapOnAll(null);
    for (var i = 0; i < array.length; i++) {
        array[i].setMap(map);
    }
}
//-----------------------------------------------------------
