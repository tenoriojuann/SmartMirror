var userChoices={
        name:"",
        email:"",
        pin:"",
        //spotifytoken: false,
        twitterwidget: false,
        mapswidget: false,
        calendarwidget:false,
        weatherwidget:true,
        clockwidget:true,
        homeAddress:"",
        workAddress:""
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
        },
        error: function(error){
            console.log(error);
        }
    });
}

//from stack overflow need to modify and test.
//From https://stackoverflow.com/questions/1255948/post-data-in-json-format
    function postIt() {
        $.ajax({
            type: "POST",
            async:false,
            url: "/register",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(userChoices),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
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
        promptAddress();
    }
    function combo(){
        createUser();
        postIt();
    }
    function promtPin(){
        var pinDel=prompt("Enter pin if you want to delete account")
        //create string to pass
        var urlString="delete/"+userChoices.email +"/"+pinDel
        $.ajax({
            type: "POST",
            async:false,
            url: "/register",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(userChoices),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            statusCode:{
                202: function(response){
                    window.location.href=urlString;
                    alert("Account Deleted");
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
    function promptAddress() {
        if (document.getElementById('eta').checked == true) {
            userChoices.homeAddress = prompt("Enter home address: ");
            userChoices.workAddress = prompt("Enter work address: ");
        }
    }
    function userInfo() {
        document.getElementById('names').innerHTML = ("User: " + userChoices.name);
        document.getElementById('email2').innerHTML = ("Email: " + userChoices.email);
        if (userChoices.clockwidget == true) {
            $('#time').bootstrapToggle('on')
        }
        if (userChoices.mapswidget == true) {
            $('#eta').bootstrapToggle('on')
        }
        if (userChoices.weatherwidget == true) {
            $('#weather').bootstrapToggle('on')
        }
        if (userChoices.calendarwidget == true) {
            $('#calendar').bootstrapToggle('on')
        }
        if (userChoices.twitterwidget == true) {
            $('#twitter').bootstrapToggle('on')
        }
    }
