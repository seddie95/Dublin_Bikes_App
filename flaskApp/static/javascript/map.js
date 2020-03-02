   function initMap() {
       //get static data for bike stations using fetch
       fetch('http://127.0.0.1:5000/static')
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
               //loop through static data to create markers for the map
               for (let i = 0; i < staticData.length; i++) {

                   // set the position of the markers using the longitude and latitude of the station
                   var marker = new google.maps.Marker({
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
                           url: "/static//icons/bikeIcon.png",
                           scaledSize: new google.maps.Size(40, 40),
                       },
                       animation: google.maps.Animation.Drop
                   });

               }

           })
           // catch used to test if something went wrong when parsing or in the network
           .catch(function (error) {
               console.error("Somethings wrong:", error);
               console.error(error);
           });

   }
