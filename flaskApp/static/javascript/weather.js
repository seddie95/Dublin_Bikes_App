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
    'Dust': "/static//icons/Haze.png",
    'Ash': "/static//icons/Haze.png",
    'Squall': "/static//icons/Haze.png",
}



function fetchWeather() {
    // function to call the weather api and display weather icons and temperature in html
    fetch('http://api.openweathermap.org/data/2.5/weather?id=7778677&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric')
        .then(function (response) {
            return response.json();
        }).then(function (obj) {
            // select the weather data from the objects
            console.log(obj)
            weathertype = obj.weather[0].main
            tempVal = obj.main.temp
            temp = parseInt(tempVal).toString() + "°c"

            // display the weather icon that correspodns to the weather type
            if (weathertype in image_dict) {
                document.getElementById("weatherIcon").src = image_dict[weathertype];

            }
            // if the weather type is not available display clouds by default
            else {
                document.getElementById("weatherIcon").src = image_dict.Clouds;
            }
            // display the temperature by updating the html of the span with id "temperature"
            document.getElementById("temperature").innerHTML = temp;
        })
}
fetchWeather()
