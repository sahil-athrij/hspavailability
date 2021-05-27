let ipsearchurl = `https://ipapi.co/${ip}/json/`

console.log(ipsearchurl)

function GetIp() {
    $.ajax(ipsearchurl,{

        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            $.ajax('/v2/getlocation',{
                success:function (data){
                    console.log(data)
                }
            })
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