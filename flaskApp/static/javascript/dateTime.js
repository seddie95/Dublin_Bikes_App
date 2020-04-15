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

                    var URL = $SCRIPT_ROOT + "/predict?date="+ date + "&time=" + time +"&station=" + station;

                // Send input data to ml model and retrieve prediction
               fetch(URL)
               .then(function (response) {
                       return response.json();
                       // use the static data to create dictionary
                   }).then(function (obj) {
                   prediction = obj.predictions;
                   /// Display bike availability prediction

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
                   })
                   // catch used to test if something went wrong when parsing or in the network
                .catch(function (error) {
                    console.error("Difficulty fetching prediction data:", error);
                    alert("Difficulty retrieving prediction, please try again later. ");
                });

                }
        })