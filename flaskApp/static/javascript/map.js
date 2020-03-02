    function initMap() {
        //get static data for bike stations using fetch
        fetch('http://127.0.0.1:5000/static')
            .then(function(response) {
                return response.json();
            }).then(function(obj) {
                staticData = obj.available

                //setting the coordinates for the map
                var location = {
                    lat: 53.348071,
                    lng: -6.268233
                };

                var map = new google.maps.Map(document.getElementById("map"), {
                    zoom: 13,
                    center: location
                });
                for (let i = 0; i < staticData.length; i++) {

                    var marker = new google.maps.Marker({
                        position: {
                            lat: parseFloat(staticData[i].Pos_Lat),
                            lng: parseFloat(staticData[i].Pos_Lng)
                        },
                        map: map,
                        title: staticData[i].Stop_Name,
                        station_number: staticData[i].Stop_Number.toString()
                    });
                }

            })
            // catch used to test if something went wrong when parsing or in the network
            .catch(function(error) {
                console.error("Somethings wrong:", error);
                console.error(error);
            });

    }