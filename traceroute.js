//takes html input and makes a call to server for traceroute
function traceroute(host)
{
    //get title and clear it
    var resultsTitle = document.getElementById("resultsTitle");
    resultsTitle.innerHTML = "";

    //get body and clear it
    var resultsBody = document.getElementById("resultsBody");
    resultsBody.innerHTML = "";

    resultsTitle.innerHTML += "Results for " + host.value;

    var $j = jQuery.noConflict();

    let tracertServerHost = "http://127.0.0.1:5000/request";

    $j.ajax({
        url: tracertServerHost,
        type: "POST",
        data: {
            request : host.value
        }
    })
    .done(function(response){
        console.log(response);
        resultsBody.innerHTML += response["result"];
    });
}


function plotPoint(latitude, longitude) {

    console.log("hello");
    const myLatLng = { lat: parseFloat(latitude), lng: parseFloat(longitude) };
    const map = new google.maps.Map(document.getElementById("map"), {
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
    //print visitors IP
    $(document).ready(()=>{
        $.getJSON("https://api.ipify.org?format=json",
        function (data) {
            // Displayin IP address on screen
            $("#gfg").html(data.ip);
        })
    });

    

    //listen for input
    var inputForm = document.getElementById("inputForm");
    inputForm.addEventListener("submit", (e) => {
        e.preventDefault();
        traceroute(document.getElementById("host"));
    });
}
