//takes html input and makes a call to server for traceroute
function traceRoute(host)
{
    //get title and clear it
    var resultsTitle = document.getElementById("resultsTitle");
    resultsTitle.innerHTML = "";

    //get body and clear it
    var resultsBody = document.getElementById("resultsBody");
    resultsBody.innerHTML = "";

    resultsTitle.innerHTML += "Results for " + host.value;
    
    var $j = jQuery.noConflict();

    var tracertServerHost = "http://127.0.0.1:5000/request";

    $j.ajax({
        url: tracertServerHost,
        type: 'POST',
        data: host.value,
        dataType: 'text',
        success: function(response)
        {
            resultsBody += response;
        }
        }
    );
}


function main()
{
    //listen for input
    var inputForm = document.getElementById("inputForm");
    inputForm.addEventListener("submit", (e) => {
        e.preventDefault();
        traceRoute(document.getElementById("host"));
    });
}

main();