// dictionary with weather types and corresponding weather icons paths
image_dict = {
    'Clear': "/static//icons/Sun.png",
    'Clouds': "/static//icons/Cloud.png",
    'Rain': "/static//icons/Rain.png",
    'Snow': "/static//icons/Snow.png",
    'Thunderstorm': "/static//icons/Storm.png",
    'fog': "/static//icons/Haze.png",
    'Mist': "/static//icons/Haze.png",
    'Smoke': "/static//icons/Haze.png",
    'Haze': "/static//icons/Haze.png",
    'Dust': "/static//icons/Haze.png",
    'Fog': "/static//icons/Haze.png",
    'Sand': "/static//icons/Haze.png",
    'Ash': "/static//icons/Haze.png",
    'Squall': "/static//icons/Haze.png",
};

function fetchWeather() {

    // function to call the weather api and display weather icons and temperature in html
    fetch('http://ec2-34-207-166-153.compute-1.amazonaws.com/weather',{
            method: "POST",
            credentials: "include",
            body: JSON.stringify(""),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            return response.json();
        }).then(function (obj) {

            // select the weather data from the objects
            var weathertype = obj.weather[0].main;
            console.log(weathertype)

            var tempVal = obj.main.temp;
            var temp = parseInt(tempVal).toString() + "°c";
            tempVal = obj.main.feels_like;
            var tempFeeling = parseInt(tempVal).toString() + "°c";

            var humidityVal = obj.main.humidity;
            var humidity = parseInt(humidityVal).toString() + "%";

            var windVal = obj.wind.speed ;
            windVal = Math.round(windVal * 3.6);
            var wind = parseInt(windVal).toString() + "Km/h";

            var date = new Date(obj.sys.sunrise * 1000);
            // Hours part from the timestamp
            var hours = date.getHours();
            // Minutes part from the timestamp
            var minutes = "0" + date.getMinutes();
            // Seconds part from the timestamp
            var seconds = "0" + date.getSeconds();
            // Will display time in 10:30:23 format
            var sunrise = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

            var date = new Date(obj.sys.sunset * 1000);
            // Hours part from the timestamp
            var hours = date.getHours();
            // Minutes part from the timestamp
            var minutes = "0" + date.getMinutes();
            // Seconds part from the timestamp
            var seconds = "0" + date.getSeconds();
            // Will display time in 10:30:23 format
            sunset = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

            document.getElementById("sunriseVal").innerHTML = sunrise;
            document.getElementById("sunsetVal").innerHTML = sunset;
            document.getElementById("temperatureVal").innerHTML = temp;
            document.getElementById("tempFeelingVal").innerHTML = tempFeeling;
            document.getElementById("humidityVal").innerHTML = humidity;
            document.getElementById("windVal").innerHTML = wind;

            // display the weather icon that corresponds to the weather type
            if (weathertype in image_dict) {
                document.getElementById("weatherIcon").src = image_dict[weathertype];
            }
            // if the weather type is not available display clouds by default
            else {
                document.getElementById("weatherIcon").src = image_dict.Clouds;
            }
        })

        // catch used to test if something went wrong when parsing or in the network
        .catch(function (error) {
           console.error("Difficulty Connecting to Weather API:", error);
        });

    //update weather every 5 minutes
    setTimeout(fetchWeather, 60000*5);
}

