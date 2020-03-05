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
               // set the map to be equal to the div with id "map"
               var map = new google.maps.Map(document.getElementById("map"), {
                   zoom: 13,
                   center: location
               });
               // create an infowindow
               var infowindow = new google.maps.InfoWindow();

               //loop through static data to create markers for the map
               var marker,i;
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

                       // set the icon of the to the bike icon  and scale it
                       icon: {
                           url: icon,
                           scaledSize: new google.maps.Size(40, 40)
                       },
                       animation: google.maps.Animation.DROP
                   });

                    // add listener to zoom to the location of the marker and display content
                    google.maps.event.addListener(marker, 'click', (function(marker, i) {
                            return function() {
                              map.setZoom(17);
                              infowindow.setContent(
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

           })
           // catch used to test if something went wrong when parsing or in the network
           .catch(function (error) {
               console.error("Somethings wrong:", error);
               console.error(error);
           });

   }

