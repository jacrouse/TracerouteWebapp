let map;


async function initMap() 
{
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: 34.891861177191906, lng : -82.42405517910554},
    zoom: 5,
  });
}

window.initMap = initMap;

initMap();
