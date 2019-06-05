"use strict";

/**
 * Use the browser's geolocation API to get the location of a user.
 *
 * For reference, here's documentation on the GeoLocation API:
 * https://developer.mozilla.org/en-US/docs/Web/API/Geolocation
 */

function success(pos){
  var crd = pos.coords; 

  fetch('/user_geolocation', {
          method: 'POST', 
          body: JSON.stringify({lat: crd.latitude, lng: crd.longitude}), 
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
  })
}


function error(err) {
  console.warn('ERROR(${err.code}): ${err.message}'); 
}

function geolocate() {
  navigator.geolocation.getCurrentPosition(success, error); 
}

let btn = document.getElementById("btn_geolocate"); 

btn.addEventListener("click", geolocate)