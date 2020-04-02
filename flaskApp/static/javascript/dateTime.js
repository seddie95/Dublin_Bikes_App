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
                var station = document.getElementById("stops-dd").value;

                console.log(station);

                var URL = "http://127.0.0.1:5000/predict?date="+ date + "&time=" + time +"&station=" + station;

                  //get weekly data for bike stations using fetch
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
                   predictions = obj.predictions;
                   console.log(predictions);

                   });

        })