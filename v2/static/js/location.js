let ipsearchurl = `http://api.ipstack.com/${ip}?access_key=a9bf777070b0b0feda3eb80895bdaa86`

console.log(ipsearchurl)

function GetIp() {
    $.ajax({
        'url': ipsearchurl,
        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            console.log(data)
        }
    })
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        console.log(position);
    }, function () {
        GetIp()
    });

} else {
    GetIp()
}