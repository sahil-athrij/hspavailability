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
    var coor = map.getCenter()

    let lat = coor.lat(), lng = coor.lng()
    {
        console.log(lat, lng)
    }
    let p = 1;

    function getData() {
        var oxy = $('input[name="oxyfr"]:checked').val() | 0
        var qry = $('input[name="query"]').val()
        var fin = $('input[name="financialfr"]:checked').val() | 0
        var vent = $('input[name="ventfr"]').val()| 0
        var oxya = $('input[name="oxyafr"]').val()| 0
        var icu = $('input[name="icufr"]').val()| 0
        var costmin = $('input[name="price-min"]').val()| 0
        var costmax = $('input[name="price-max"]').val()| 0
        var care = $('input[name="carefr"]:checked').val()| 0
        var covid = $('input[name="covidfr"]:checked').val()| 0
        var bed = $('input[name="bedf"]').val()| 0
        dict = {
            search:qry,
            financial_rating__gte: parseInt(fin),
            oxygen_rating__gte: parseInt(oxy),
            ventilator_availability__gte: parseInt(vent),
            oxygen_availability__gte: parseInt(oxya),
            icu_availability__gte: parseInt(icu),
            avg_cost__gte: parseInt(costmin),
            avg_cost__lte: parseInt(costmax),
            care_rating__gte: parseInt(care),
            covid_rating__gte: parseInt(covid),
            beds_available__gte: parseInt(bed)
        }

        Marker.filter(kwargs = {
            lat__gte: lat - 1, lat__lte: lat + 1, lng__gte: lng - 1,
            lng__lte: lng + 1, page: p, ...dict
        }).then(function (markerList) {
            let i;
            ob = markerList;
            console.log(ob);
            for (i = 0; i < ob.results.length; i++) {
                {
                    console.log((p - 1) * 100 + i + 1, ob.results[i].name)
                }
                addMarker({
                    'position': {
                        'lat': ob.results[i].lat,
                        'lng': ob.results[i].lng,
                    },
                    'size': ob.results[i].size,
                    'id': ob.results[i].id
                })
            }
            p++;
            if (markerList.next) {
                getData();
            }
        })
    }

    getData();
}


function filldata(id) {

    Marker.get(id, kwargs).then(function (data) {
        console.log(data)
        $('#valuetitle').text(data.name)
        $('input:radio[name=valuecon]').val([parseInt(data.care_rating)])
        $('input:radio[name=valueaff]').val([parseInt(data.financial_rating)])
        $('input:radio[name=valuecov]').val([parseInt(data.covid_rating)])
        $('input:radio[name=valueoxy]').val([parseInt(data.oxygen_rating)])
        $('#valueoxy_output').text(data.oxygen_rating)
        $('#valuecov_output').text(data.covid_rating)
        $('#valueaff_output').text(data.financial_rating)
        $('#valuecon_output').text(data.care_rating)

        $('#valuecost').text(data.avg_cost)
        $('#valueventa').text(data.ventilator_availability)
        $('#valueoxya').text(data.oxygen_availability)
        $('#valueicu').text(data.icu_availability)

        $('#valueredirect').attr('href', `/v2/details/${data.id}`)
        $('#phone').html(data.Phone)
        $('#phone').attr("href", 'tel:' + data.Phone)


        $('#id').val(data.id)
        $('#ids').val(data.id)
    })
}


var element = document.getElementById("map");
var cen;
map = new google.maps.Map(element, {
    zoom: 12,
    mapTypeId: "OSM",
    mapTypeControl: false,
    streetViewControl: false,

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

