var map;
      var directionDisplay;
      var directionsService;
      var stepDisplay;
      var markerArray = [];

      function initialize() {
        // Instantiate a directions service.
        directionsService = new google.maps.DirectionsService();
       alert("Hello World")

        // Create a map and center it on Manhattan.
        var manhattan = new google.maps.LatLng(5.6045400000000001, -0.17802000000000001);
        var mapOptions = {
          zoom: 15,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          center: manhattan
        }
        map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

        // Create a renderer for directions and bind it to the map.
        var rendererOptions = {
          map: map
        }
        directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)

        // Instantiate an info window to hold step text.
        stepDisplay = new google.maps.InfoWindow();
      }

      function calcRoute() {

        // First, remove any existing markers from the map.
        for (i = 0; i < markerArray.length; i++) {
          markerArray[i].setMap(null);
        }

        // Now, clear the array itself.
        markerArray = [];

        // Retrieve the start and end locations and create
        // a DirectionsRequest using WALKING directions.
        var start = document.getElementById('start').value;
        var end = document.getElementById('end').value;
        var request = {
            origin: start,
            destination: end,
            travelMode: google.maps.DirectionsTravelMode.DRIVING
        };

        // Route the directions and pass the response to a
        // function to create markers for each step.
        directionsService.route(request, function(response, status) {
          if (status == google.maps.DirectionsStatus.OK) {
            var warnings = document.getElementById('warnings_panel');
            warnings.innerHTML = '<b>' + response.routes[0].warnings + '</b>';
            directionsDisplay.setDirections(response);
            showSteps(response);
          }
        });
      }

      function showSteps(directionResult) {
        // For each step, place a marker, and add the text to the marker's
        // info window. Also attach the marker to an array so we
        // can keep track of it and remove it when calculating new
        // routes.
        var myRoute = directionResult.routes[0].legs[0];

        for (var i = 0; i < myRoute.steps.length; i++) {
          var marker = new google.maps.Marker({
            position: myRoute.steps[i].start_point,
            map: map
          });
          attachInstructionText(marker, myRoute.steps[i].instructions);
          markerArray[i] = marker;
        }
      }

      function attachInstructionText(marker, text) {
        google.maps.event.addListener(marker, 'click', function() {
          // Open an info window when the marker is clicked on,
          // containing the text of the step.
          stepDisplay.setContent(text);
          stepDisplay.open(map, marker);
        });
      }

