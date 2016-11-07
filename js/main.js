'use strict';

$(function() {
    var map = L.map('map');
    map.setView([39.50, -98.35], 3);
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmljaGFyZGRpbmciLCJhIjoiY2l2N3M3NWY0MDAyNDJ0cGJsejdmOXN2cyJ9.RaIxdkH4qDQrGtfHDkcCWg', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 100,
        id: 'richardding.223065kd',
        accessToken: 'pk.eyJ1IjoicmljaGFyZGRpbmciLCJhIjoiY2l2N3NucTc5MDAxaTJvcGNhN2k1bHdodiJ9.APG6g1898a3Z3g1uCQ7qgw'
    }).addTo(map);
});