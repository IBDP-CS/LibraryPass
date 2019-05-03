
$(document).ready(function(){
  var state1 = 0;

  console.log(state1);
  console.log(Cookies.get());
  var stuid = Cookies.get("stuid");
  document.getElementById("stuid").innerHTML = "Welcome<br><h3>"+stuid+"</h3>";

  $.post("/get-state",{
    id: stuid,
  },
  function(request){
    if (request.code){
      alert("An Unexpected Error has occured. Please Refresh the Page and Try Again");
    }
    else{
      var sState = request.data;
      switch (sState) {
        case 0:
          document.getElementById("state").innerHTML = "Not Signed Up";
          break;
        case 1:
          document.getElementById("state").innerHTML = "Wait For Approval";
          break;
        case 2:
          document.getElementById("state").innerHTML = "Request Approved";
          break;
        case 3:
          document.getElementById("state").innerHTML = "In Library";
          break;
        case 4:
          document.getElementById("state").innerHTML = "Going back to Dorm";
          break;

        default: document.getElementById("state").innerHTML = NULL;

      }
    }
  });

  $("#bookMe").click(function(){
    state1 = 1;

    $.post("/update-state",{
      id: stuid,
      state: state1,
    },
    function(data){
    if (data.code){
      alert("An Unexpected Error has occured. Please Refresh the Page and Try Again");
    }else{
      alert("You signed up");
    }
  });
    console.log(state1);
  });
});
