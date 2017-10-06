var userChoices={
        name:"name" ,
        email:"rando@gmail.com",
        googletoken:"temp",
        pin:"temp",
        spotifytoken: false,
        twittertoken: false,
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
function spotifytoken(){
    if(document.getElementById('spotifytoken').checked) {
        userChoices.spotifytoken=true;
    } else {
        userChoices.spotifytoken=false;
}
}
function maps(){
    if(document.getElementById('maps').checked) {
        userChoices.weather=true;
    } else {
        userChoices.weather=false;
}
}
function twittertoken(){
    if(document.getElementById('twittertoken').checked) {
        userChoices.twittertoken=true;
    } else {
        userChoices.twittertoken=false;
}
}
function weather() {
    if (document.getElementById('weather').checked) {
        userChoices.time = true;
    } else {
        userChoices.time = false;
    }
}
//Doesn't work
function googletoken() {
    userchoices.googletoken= url_for('');

}
function pin(){
    userChoices.pin=document.getElementById('pin').value;
}
function name(){
    userChoices.name="fromGoogleToken"

}
function email(){
    userChoices.email="fromGoogleToken"
}
function facePath(){
    document.getElementById('facepath').files;
}
//from stack overflow need to modify and test.
function postIt(){
  // construct an HTTP request
  var xhr = new XMLHttpRequest();
  xhr.open(form.method, form.action, true);
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

  // send the collected data as JSON
  xhr.send(JSON.stringify(userChoices));

  xhr.onloadend = function () {
    // done
  };
    //different method
    //$('#userChoices').val(JSON.stringify(userChoices));
   // $('form').submit();
}
function createUser(){
    email();
    name();
    time();
    googletoken();
    pin();
    weather();
    twittertoken();
    maps();
    spotifytoken();
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