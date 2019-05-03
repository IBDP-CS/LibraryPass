$(document).ready(function(){

  $("#login").click(function(){
    var username1 = $("#username").val();
    var password1 = $("#password").val();

    var st = username1.split('s');
    var num = st[1];

    if (!isNaN(num)){
      var state = "student";

    }
    else var state = "teacher";

    console.log(state);

    $.post("http://libpass.georgeyu.cn/login",{
      username: username1,
      password: password1
    },

    function(data){
      if (data.code){
        alert("Your Password is Incorrect!");
      }
      else{
        alert("You successfully logged in.");

        Cookies.set('stuid', username1);

        console.log(Cookies.get());
        if (state == "student") window.location.href = "studentpage.html";
        else if (state == "teacher") window.location.href = "teacherpage.html";
        else if (state == "libraryTeacher") window.location.href = "librarypage.html";
      }
    });
   });
 });
