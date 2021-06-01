// put all the global variables here
let url_string = window.location.href
let url = new URL(url_string);
let ipsearchurl = `https://ipapi.co/${ip}/json/`
let latitude = ''
let longitude = ''
let map = ''//complex object of type OpenLayers.Map
let dict = {};

let state = {}



locationiq.key = 'pk.959200a41370341f608a91b67be6e8eb';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function GetIp() {
    $.ajax(ipsearchurl, {

        success: function (data) {
            latitude = data.latitude
            longitude = data.longitude
        },
        error: function (data) {
            $.ajax('/v2/getlocation', {
                success: function (data) {
                    latitude = data.latitude
                    longitude = data.longitude
                    $('#lat').val(latitude)
                    $('#lng').val(longitude)
                }
            })
        }
    })
}

function setupLatLng() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            console.log(position);
            latitude = position.coords.latitude
            longitude = position.coords.longitude
            $('#lat').val(latitude)
            $('#lng').val(longitude)
        }, function () {
            GetIp()
        });

    } else {
        GetIp()
    }
}