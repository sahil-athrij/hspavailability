let latleft = 0
let latright = 0
let longtop = 0
let longbottom = 0


function setBoundBox(latitude, longitude) {
    latleft = Math.round(((latitude + Number.EPSILON) * 10) - 1) / 100
    latright = Math.round(((latitude + Number.EPSILON) * 10) + 1) / 100
    longtop = Math.round(((longitude + Number.EPSILON) * 10) - 1) / 100
    longbottom = Math.round(((longitude + Number.EPSILON) * 10) + 1) / 100
}

let markers = [];

function addMarker(feature) {
    const marker = new google.maps.Marker({
        position: feature.position,
        icon: icons[feature.size],
        map: map
    });
    markers.push(marker);
    marker.addListener('click', function () {
        filldata(feature.id)
    });
}

function setMapOnAll(map) {
    for (i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function deleteMarkers() {
    setMapOnAll(null);
    markers = [];
}

function getMarkers() {
    const csrftoken = getCookie('csrftoken');
    var coor = map.getCenter()
    var LatLon = {csrfmiddlewaretoken: csrftoken, lat: coor.lat(), lng: coor.lng()}
    console.log(LatLon)
    $.ajax({
        type: 'POST',
        url: `/markers/`,
        dataType: 'json',
        data: LatLon,
        success: function (data) {
            var i;
            ob = data;
            for (i = 0; i < ob.length; i++) {
                addMarker({
                    'position': {
                        'lat': ob[i].lat,
                        'lng': ob[i].lng,
                    },
                    'size': ob[i].size,
                    'id': ob[i].id
                })
            }
        }
    })
}

function filldata(id) {
    $.ajax({
        url: `/more_info/${id}/`,
        success: function (data) {

            console.log(data)
            $('#header').text(data.name)
            $('#phone').html(data.Phone)
            $('#phone').attr("href", 'tel:' + data.Phone)
            $('input:radio[name=ratingm]').val([parseInt(data.care_rating)])
            $('#ratingf').text(data.care_rating)
            $('input:radio[name=covidm]').val([parseInt(data.covid_rating)])
            $('#covidf').text(data.covid_rating)
            $('input:radio[name=oxym]').val([parseInt(data.oxygen_rating)])
            $('#oxyf').text(data.oxygen_rating)
            $('#vent').text(data.ventilator_availability)
            $('#oxya').text(data.oxygen_availability)
            $('#icu').text(data.icu_availability)
            $('input:radio[name=financialm]').val([parseInt(data.financial_rating)])
            $('#financialf').text(data.financial_rating)
            $('#beds').text(data.beds_available)
            $('#cost').text(data.avg_cost)
            $('#id').val(data.id)
            $('#ids').val(data.id)
        }
    })
}


let map; //complex object of type OpenLayers.Map

var element = document.getElementById("map");
var cen;
map = new google.maps.Map(element, {
    zoom: 12,
    mapTypeId: "OSM",
    mapTypeControl: false,
    streetViewControl: false
});

map.setCenter({lat: latitude, lng: longitude})
initialLocation = new google.maps.LatLng(latitude, longitude);
cen = initialLocation;

getMarkers()
setBoundBox(latitude, longitude)


map.mapTypes.set("OSM", new google.maps.ImageMapType({
    getTileUrl: function (coord, zoom) {
        // "Wrap" x (longitude) at 180th meridian properly
        // NB: Don't touch coord.x: because coord param is by reference, and changing its x property breaks something in Google's lib
        var tilesPerGlobe = 1 << zoom;
        var x = coord.x % tilesPerGlobe;
        if (x < 0) {
            x = tilesPerGlobe + x;
        }
        // Wrap y (latitude) in a like manner if you want to enable vertical infinite scrolling
        return "https://tile.openstreetmap.org/" + zoom + "/" + x + "/" + coord.y + ".png";
    },
    tileSize: new google.maps.Size(256, 256),
    name: "OpenStreetMap",
    maxZoom: 18
}));


google.maps.event.addListener(map, 'dragend', function () {
    var coor = map.getCenter();

    if (coor.lat() > (cen.lat() + 1) || coor.lat() < (cen.lat() - 1) || coor.lng() > (cen.lng() + 1) || coor.lng() < (cen.lng() - 1)) {
        deleteMarkers();
        getMarkers();
        cen = coor;
    }
});

