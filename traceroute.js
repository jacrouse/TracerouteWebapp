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

    let tracertServerHost = "http://127.0.0.1:5000/request";

    //get visitor IP
    $j.ajax({
        url: tracertServerHost,
        type: "GET",
        datatype: "jsonp",
        crossDomain:true,
    })
    .done(function(response){
        let contents = response["result"];
        userIP.innerHTML += contents;
    });

    $j.ajax({
        url: tracertServerHost,
        type: "POST",
        datatype: "jsonp",
        crossDomain:true,
        data: {
            request : host.value
        }
    })
    .done(function(response){
        let contents = response["result"];
        resultsBody.innerHTML += contents;

        //extract coordinates and plot them
        let instances = contents.split("<br>");

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

            plotPoint(lat, lng);
        }
        
    });
}


function plotPoint(latitude, longitude) {
    var myLatLng = { lat: parseFloat(latitude), lng: parseFloat(longitude) };
    var map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: myLatLng,
    });
    
  
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
