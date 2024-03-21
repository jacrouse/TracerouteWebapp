//takes html input and makes a call to server for traceroute
function traceroute(host)
{
    //get user IP and clear it
    var userIP = document.getElementById("gfg");
    userIP.innerHTML = "";
    userIP.innerHTML = "Your IP address is:<br>";

    //get title and clear it
    var resultsTitle = document.getElementById("resultsTitle");
    resultsTitle.innerHTML = "";

    //get body and clear it
    var resultsBody = document.getElementById("resultsBody");
    resultsBody.innerHTML = "";

    resultsTitle.innerHTML += "Please be patient, this can take a while.<br>"
    resultsTitle.innerHTML += "Results for: " + host.value;

    var $j = jQuery.noConflict();

    let tracertServerHost = "https://167.99.0.220:5000/request";

    //get visitor IP
    $j.ajax({
        url: tracertServerHost,
        type: "GET",
        datatype: "jsonp",
        xhrFields: {
        	withCredentials: true
        },
        crossDomain:true,
     	contentType: 'application/json; charset=utf-8'
    })
    .done(function(response){
        let contents = response["result"];
        userIP.innerHTML += contents;
    });

    $j.ajax({
        url: tracertServerHost,
        type: "POST",
        datatype: "jsonp",
        xhrFields: {
        	withCredentials: true
        },
        crossDomain:true,
        contentType: 'applications/json; charset=utf-8',
        data: {
            request : host.value
        }
    })
    .done(function(response){
        let contents = response["result"];
        resultsBody.innerHTML += contents;

        //extract coordinates and plot them
        let instances = contents.split("<br>");

        var map = new google.maps.Map(document.getElementById("map"), {
            zoom: 3,
            center: { lat: 0.0, lng: 0.0 },
        });

        var path = [];

        for(var i = 0; i < instances.length; i++)
        {
            let splitContents = instances[i].split(' ');
            let coordsIndex = splitContents.indexOf("Coords:");

            if(coordsIndex == -1 || coordsIndex + 2 > instances[i].length)
                continue;

            let lat = splitContents[coordsIndex + 1].replace('[','');
            var lng = ""; 

            //account for if there is anything between them
            if((coordsIndex + 2) < (splitContents.length) && splitContents[coordsIndex + 2] == "")
                lng = splitContents[coordsIndex + 3].replace(']','');
            else
                lng = splitContents[coordsIndex + 2].replace(']','');

            //check if no valid coords returned
            if(lat == "'NoLat'," || lng == "'NoLng'")
                continue;

            plotPoint(map, lat, lng);
            path.push({"lat" : parseFloat(lat), "lng" : parseFloat(lng)});
        }

        const outPath = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 2
        });
        
        outPath.setMap(map);
    });
}


function plotPoint(map, latitude, longitude) {
    var myLatLng = { lat: parseFloat(latitude), lng: parseFloat(longitude) };
  
    new google.maps.Marker({
      position: myLatLng,
      map,
      title: "Hello World!",
    });
}


function traceroute_main()
{
    //listen for input
    var inputForm = document.getElementById("inputForm");
    inputForm.addEventListener("submit", (e) => {
        e.preventDefault();
        traceroute(document.getElementById("host"));
    });
}
