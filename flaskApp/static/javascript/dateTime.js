   $(document).ready(function(){
          var minDate = new Date();
          $("#pdate").datepicker({
              //showAnim: 'drop'
              numberofMonth:1,
              minDate:minDate,
              maxDate:5,
              dateFormat:'dd/mm/yy'

          });

      });
          $(document).ready(function(){
              $('#ptime').timepicker({
                    timeFormat: 'H:mm',
                    interval: 30,
                    minTime: '0',
                    maxTime: '23:30',
                    startTime: '0',
                    dynamic: false,
                    dropdown: true,
                    scrollbar: true
                });

          });

//-----------------------------------------------------------------------
// function to pass form data to flask
 const myForm = document.getElementById("predictionData");
        myForm.addEventListener("submit",(e) =>{
                //Prevent the page from refreshing
                e.preventDefault();

                // Get form values
                var date = document.getElementById("pdate").value;
                var time = document.getElementById("ptime").value;

                if (document.getElementById("stops-dd").value == "default") {
                    alert("Please select a station from the dropdown, or click on a station on the map");
                } else {
                    var station = document.getElementById("stops-dd").value;
                    console.log(station);
                    var URL = "http://127.0.0.1:5000/predict?date="+ date + "&time=" + time +"&station=" + station;

                // Send input data to ml model and retrieve prediction
               fetch(URL,{
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
                   prediction = obj.predictions;
                   /// Display bike availability prediction
                   console.log(prediction);
                   if (prediction < 0) {
                       prediction = 1;
                   }
                   if (prediction == 1) {
                       document.getElementById("predictionOutput").innerHTML = "There should be around " +
                       prediction + " bike available at this station on " + date + " at " + time;
                   } else {
                       document.getElementById("predictionOutput").innerHTML = "There should be around " +
                       prediction + " bikes available at this station on " + date + " at " + time;
                   }
                   });
                }
        })