var state1 = 0;

console.log(state1);
console.log(Cookies.get());
var stuid = Cookies.get("stuid");
var username = Cookies.get("username");
document.getElementById("stuid").innerHTML = "Welcome, " + username + "!";

$.post("/get-state", {
        id: stuid,
    },
    function(request) {
        if (request.code) {
            alert("An Unexpected Error has occured. Please Refresh the Page and Try Again");
        } else {
            var sState = request.data;
            switch (sState) {
                case 0:
                    document.getElementById("state").innerHTML = "In dorm";
                    $("#bookMe").removeAttr("disabled");
                    break;
                case 1:
                    document.getElementById("state").innerHTML = "Waiting for approval";
                    break;
                case 2:
                    document.getElementById("state").innerHTML = "En route to library";
                    break;
                case 3:
                    document.getElementById("state").innerHTML = "In library";
                    break;
                case 4:
                    document.getElementById("state").innerHTML = "En route to dorm";
                    break;
                default:
                    document.getElementById("state").innerHTML = "Unknown";

            }
        }
    });

$("#bookMe").click(function() {
    state1 = 1;

    $.post("/update-state", {
            id: stuid,
            state: state1,
        },
        function(data) {
            if (data.code) {
                alert("An Unexpected Error has occured. Please Refresh the Page and Try Again");
            } else {
                alert("You request is sent");
                $("#bookMe").attr("disabled", "");
            }
        });
    console.log(state1);
});
