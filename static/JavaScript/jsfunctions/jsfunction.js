var userChoices={
        name:"name" ,
        email:"rando@gmail.com",
        pin:"temp",
        //spotifytoken: false,
        twitterWidget: false,
        mapWidget: false,
        calendarWidget:false,
        weatherWidget:true,
        clockWidget:true
    };

function time(){
    if(document.getElementById('time').checked) {
        userChoices.clockWidget=true;
    } else {
        userChoices.clockWidget=false;
}
}
function calendar(){
    if(document.getElementById('calendar').checked) {
        userChoices.calendarWidget=true;
    } else {
        userChoices.calendarWidget=false;
}
}
//function spotifytoken(){
   // if(document.getElementById('spotifytoken').checked) {
     //   userChoices.spotifytoken=true;
    //} else {
    //    userChoices.spotifytoken=false;
//}
//}
function maps(){
    if(document.getElementById('eta').checked) {
        userChoices.mapWidget=true;
    } else {
        userChoices.mapWidget=false;
}
}
function twitter(){
    if(document.getElementById('twitter').checked) {
        userChoices.twitterWidget=true;
    } else {
        userChoices.twitterWidget=false;
}
}
function weather(){
    if (document.getElementById("weather").checked) {
        userChoices.weatherWidget=true;
    } else {
        userChoices.weatherWidget=false;
}
}

function pin(){
    userChoices.pin=document.getElementById('pin').value;
}
function name(){
    userChoices.name="fromEndPoint"

}
function email(){
    userChoices.email="fromEbdPoint"
}

//from stack overflow need to modify and test.
//From https://stackoverflow.com/questions/1255948/post-data-in-json-format
function postIt() {
$.ajax({
   type: "POST",
   url: "/register",
   // The key needs to match your method's input parameter (case-sensitive).
   data: JSON.stringify(userChoices),
   contentType: "application/json; charset=utf-8",
   dataType: "json",
   success: function(data){alert(data);},
   failure: function(errMsg) {
       alert(errMsg);
   }
});
}
function createUser(){
    email();
    name();
    time();
    pin();
    weather();
    twitter();
    maps();
    calendar();

}