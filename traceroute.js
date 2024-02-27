//takes html input and makes a call to server for traceroute
function traceRoute(host)
{
    document.getElementById("resultsTitle").innerHTML += "Results for: " + host.value;

    //tracert will go here

    document.getElementById("resultsBody").innerHTML += "results body";
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