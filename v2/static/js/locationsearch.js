let lat = url.searchParams.get("lat")
let lng = url.searchParams.get("lng")
let query = url.searchParams.get("query")
let loc = url.searchParams.get("loc")

if (lat) {
    $('#lat').val(parseFloat(lat))
    latitude = parseFloat(lat)
}
if (lng) {
    $('#lng').val(parseFloat(lng))
    longitude = parseFloat(lng)
}
if (query) {
    $('#hspsearch').val(query)
}

function checkSearchResults() {
    let error = $('.mapbox-gl-geocoder--no-results').html()
    if (error) {
        fetch(`https://us1.locationiq.com/v1/search.php?key=${locationiq.key}&q=${value}&countrycodes=in&format=json`).then(r => {
            console.log(r)
            if (r.status < 300) {
                r.json().then(r => {
                    console.log(r)
                    let item = r[0]
                    latitude = parseFloat(item.lat)
                    longitude = parseFloat(item.lon)
                    $('#lat').val(latitude)
                    $('#lng').val(longitude)
                    $('#bottomsearch button')[0].click()
                })
            } else {
                addToast('Failed Location Search', 'Unable to Find the location, Please Try Again')
            }
        })
    } else {

        $('#bottomsearch button')[0].click()
    }
}

var geocoder = new MapboxGeocoder({
    accessToken: locationiq.key,
    limit: 5,
    dedupe: 1,
    countrycodes: 'in',
    className: 'input-right',
    placeholder: 'Location (Auto)',
    getItemValue: function (item) {
        latitude = parseFloat(item.lat)
        longitude = parseFloat(item.lon)
        $('#lat').val(latitude)
        $('#lng').val(longitude)
        if (typeof map === 'object') {
            map.setCenter({lat: item.center[1], lng: item.center[0]})
        }
        if (typeof getMarkers === "function") {
            getMarkers()
        }
        $('#bottomsearch button')[0].click()
        return item.place_name

    }
});
geocoder.addTo('#search-box');

$('#hspsearch').on('keydown', function (event) {
    if (event.key === "Enter") {
        event.preventDefault()
        checkSearchResults()

        return false;
    }
})
$($('.mapboxgl-ctrl-geocoder--input')[0]).on('keydown', function (event) {
    if (event.key === "Enter") {
        event.preventDefault()
        checkSearchResults()
        return false;
    }
})

$('.mapboxgl-ctrl-geocoder').addClass('input-small-rounder')
$($('.mapboxgl-ctrl-geocoder')[0]).addClass('w-100 input-left')
$($('.mapboxgl-ctrl-geocoder--input')[0]).attr('name', 'loc')
$($('.mapboxgl-ctrl-geocoder--input')[0]).attr('id', 'loc')
$($('.mapboxgl-ctrl-geocoder--input')[0]).attr('autocomplete', "off")
$($('.mapboxgl-ctrl-geocoder--icon')[0]).html(`
<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
 viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
<g>
<g>
<path d="M256,0C156.748,0,76,80.748,76,180c0,33.534,9.289,66.26,26.869,94.652l142.885,230.257
c2.737,4.411,7.559,7.091,12.745,7.091c0.04,0,0.079,0,0.119,0c5.231-0.041,10.063-2.804,12.75-7.292L410.611,272.22
C427.221,244.428,436,212.539,436,180C436,80.748,355.252,0,256,0z M384.866,256.818L258.272,468.186l-129.905-209.34
C113.734,235.214,105.8,207.95,105.8,180c0-82.71,67.49-150.2,150.2-150.2S406.1,97.29,406.1,180
C406.1,207.121,398.689,233.688,384.866,256.818z"/>
</g>
</g>
<g>
<g>
<path d="M256,90c-49.626,0-90,40.374-90,90c0,49.309,39.717,90,90,90c50.903,0,90-41.233,90-90C346,130.374,305.626,90,256,90z
 M256,240.2c-33.257,0-60.2-27.033-60.2-60.2c0-33.084,27.116-60.2,60.2-60.2s60.1,27.116,60.1,60.2
C316.1,212.683,289.784,240.2,256,240.2z"/>
</g>
</g>
</svg>
`)
if (loc) {
    $($('.mapboxgl-ctrl-geocoder--input')[0]).val(loc)

}

if (!lat || !lng) {
    setupLatLng()
}

