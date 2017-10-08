var userChoices={
        name:"name" ,
        email:"rando@gmail.com",
        pin:"temp",
        //spotifytoken: false,
        twitter: false,
        maps: false,
        calendar:false,
        weather:true,
        time:true
    };

function time(){
    if(document.getElementById('time').checked) {
        userChoices.time=true;
    } else {
        userChoices.time=false;
}
}
function calendar(){
    if(document.getElementById('calendar').checked) {
        userChoices.calendar=true;
    } else {
        userChoices.calendar=false;
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
        userChoices.maps=true;
    } else {
        userChoices.maps=false;
}
}
function twitter(){
    if(document.getElementById('twitter').checked) {
        userChoices.twitter=true;
    } else {
        userChoices.twitter=false;
}
}
function weather(){
    if (document.getElementById("weather").checked) {
        userChoices.weather=true;
    } else {
        userChoices.weather=false;
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
    var form;

    form.onsubmit = function (e) {
        // stop the regular form submission
        e.preventDefault();

        // collect the form data while iterating over the inputs
        var data = userChoices;
        // construct an HTTP request
        var xhr = new XMLHttpRequest();
//Not sure about equal post or the address.
        xhr.open(form.method="post", form.action="http://127.0.0.1:5000/Register", true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

        // send the collected data as JSON
        xhr.send(JSON.stringify(data));

        xhr.onloadend = function () {
            // done
        };
    };
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
//use to test
function alert2(){
    alert(userChoices);
}
  //tested time() and printed userchoices.time
function test(){
        if (document.getElementById('time').checked)
            alert("shit hit the fan");
        else {
            facePath();
            alert(userChoices.facepath);
        }
}