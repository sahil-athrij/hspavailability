let ipsearchurl = `https://ipapi.co/${ip}/json/`
let latitude = ''
let longiude = ''
console.log(ipsearchurl)

function GetIp() {
    $.ajax(ipsearchurl, {

        success: function (data) {
            latitude = data.latitude
            longiude = data.longitude
        },
        error: function (data) {
            $.ajax('/v2/getlocation', {
                success: function (data) {
                    latitude = data.latitude
                    longiude = data.longitude
                }
            })
        }
    })
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        console.log(position);
        latitude = position.coords.latitude
        longiude = position.coords.longitude
        console.log(latitude, longiude)
    }, function () {
        GetIp()
    });

} else {
    GetIp()
}