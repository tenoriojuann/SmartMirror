var userChoices={
        name:"name" ,
        email:"rando@gmail.com",
        pin:"temp",
        //spotifytoken: false,
        twitterwidget: false,
        mapswidget: false,
        calendarwidget:false,
        weatherwidget:true,
        clockwidget:true
    };

function time(){
    if(document.getElementById('time').checked) {
        userChoices.clockwidget=true;
    } else {
        userChoices.clockwidget=false;
}
}
function calendar(){
    if(document.getElementById('calendar').checked) {
        userChoices.calendarwidget=true;
    } else {
        userChoices.calendarwidget=false;
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
        userChoices.mapswidget=true;
    } else {
        userChoices.mapswidget=false;
}
}
function twitter(){
    if(document.getElementById('twitter').checked) {
        userChoices.twitterwidget=true;
    } else {
        userChoices.twitterwidget=false;
}
}
function weather(){
    if (document.getElementById("weather").checked) {
        userChoices.weatherwidget=true;
    } else {
        userChoices.weatherwidget=false;
}
}

function pin(){
    userChoices.pin=document.getElementById('pin').value;
}
function name() {
    $.ajax({
        url: '/currentUser',
        type: "GET",
        dataType: "json",
        success: function (data) {
            userChoices.name = data.name;
            userChoices.email = data.email;
        }
    });
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
            async:false,
            statusCode:{
                202: function(response){
                    alert("Submission was successful");
                }
            },
            success: function (data) {
                alert(data);
            },
            failure: function (errMsg) {
                alert(errMsg);
            }
        });
    }

    function createUser() {
        name();
        time();
        pin();
        weather();
        twitter();
        maps();
        calendar();

    }
    function getUserData(){
        var userData
    }
    function combo(){
        createUser();
        postIt();
    }