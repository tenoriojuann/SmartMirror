/**
 * Created by Dedric on 10/8/2017.
 */
var today = {
    curHour: "",
    curMinute: "",
    curSeconds: "",
    curMeridiem: "",
    dayOfWeek: "",
    dayOfMonth: "",
    curMonth: "",
    curYear: ""
}
function date_time(id) {
    //weatherData();
    objToday = new Date(),
        weekday = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
        dayOfWeek = weekday[objToday.getDay()],
        domEnder = function () {
            var a = objToday;
            if (/1/.test(parseInt((a + "").charAt(0)))) return "th";
            a = parseInt((a + "").charAt(1));
            return 1 == a ? "st" : 2 == a ? "nd" : 3 == a ? "rd" : "th"
        }(),
        dayOfMonth = ( objToday.getDate() < 10) ? '0' + objToday.getDate() + domEnder : objToday.getDate() + domEnder,
        months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'),
        curMonth = months[objToday.getMonth()],
        curYear = objToday.getFullYear(),
        curHour = function () {
            var b = objToday.getHours();
            if (b == 13) return "1";
            if (b == 14) return "2";
            if (b == 15) return "3";
            if (b == 16) return "4";
            if (b == 17) return "5";
            if (b == 18) return "6";
            if (b == 19) return "7";
            if (b == 20) return "8";
            if (b == 21) return "9";
            if (b == 22) return "10";
            if (b == 23) return "11";
            if (b == 24) return "12";

        }(),

        curMinute = objToday.getMinutes() < 10 ? "0" + objToday.getMinutes() : objToday.getMinutes(),
        curSeconds = objToday.getSeconds() < 10 ? "0" + objToday.getSeconds() : objToday.getSeconds(),
        curMeridiem = objToday.getHours() > 12 ? "PM" : "AM";

    CurrentDate = dayOfWeek + " " + curMonth + " " + dayOfMonth + ", " + curYear;
    CurrentTime = curHour + ":" + curMinute + ":" + curSeconds + " " + curMeridiem;
    document.getElementById("date").innerHTML = CurrentDate;
    document.getElementById(id).innerHTML = CurrentTime;
    /*Uncomment for real-time clock*/
    // console.log(CurrentDate + "\n" + CurrentTime);
    setTimeout('date_time("' + id + '");', '1000');
    return true;

}

var currentWeather = {
    temp: "temp",
    imageURL: "",
    description: "",
    location: ""

}
function weatherData() {
    $.ajax({
        url: '/weather',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data);
            currentWeather.temp = data.main.temp;
            currentWeather.imageURL = data.weather[0].icon;
            currentWeather.description = data.weather[0].description;
            currentWeather.location = data.name;


            document.getElementById("location").innerHTML = currentWeather.location;
            document.getElementById("tempDegrees").innerHTML = currentWeather.temp + " °F";
            document.getElementById("description").innerHTML = currentWeather.description;
            document.getElementById("weatherIMG").src = "http://openweathermap.org/img/w/" + currentWeather.imageURL + ".png";
            setTimeout('weatherData()', 1800000); //30 minute update weather
            console.log(currentWeather);
        }
    });
}
var currentMaps = {
    destination_addresses: "",
    origin_addresses: "",
    distance: "",
    duration: ""
}
function mapsData(email) {
    $.ajax({
        url: '/maps/' + email,
        type: "GET",
        dataType: "json",
        success: function (data1) {
            console.log(data1);
            currentMaps.destination_addresses = data1.destination_addresses;
            currentMaps.origin_addresses = data1.origin_addresses;
            currentMaps.distance = data1.rows[0].elements[0].distance.text;
            currentMaps.duration = data1.rows[0].elements[0].duration.text;

            document.getElementById("destination").innerHTML = "To: " + currentMaps.destination_addresses;
            document.getElementById("origin").innerHTML = "From: " + currentMaps.origin_addresses;
            document.getElementById("distance").innerHTML = "Distance: " + currentMaps.distance;
            document.getElementById("duration").innerHTML = "ETA: " + currentMaps.duration;
        }
    });
}
var currentEvents = {

    Title: "",
    endTime: "",
    startTime: ""

}

function eventData(email) {
    $.ajax({
        url: '/events/' + email,
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data);

            for (i = 0; i < 4; i++) {
                currentEvents.Title = data[i].Title;
                currentEvents.endTime = data[i].endTime;
                currentEvents.startTime = data[i].startTime;

                document.getElementById("eventTitle" + i).innerHTML = currentEvents.Title;
                document.getElementById("eventStart" + i).innerHTML = currentEvents.startTime;
                document.getElementById("eventEnd" + i).innerHTML = currentEvents.endTime;
                console.log(data[i])
            }
        }
    })
}
var choices = {
    //spotifytoken: false,
    twitterWidget: "",
    mapWidget: "",
    calendarWidget: "",
    weatherWidget: "",
    clockWidget: ""
};

function choiceDisplay(email) {
    $.ajax({
        url: '/profile/' + email,
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data);

            choices.twitterWidget = data.twitterWidget;
            choices.mapWidget = data.mapWidget;
            choices.calendarWidget = data.calendarWidget;
            choices.weatherWidget = data.weatherWidget;
            choices.clockWidget = data.clockWidget;
            hideshow(choices);
        }
    });
}
function hideshow(choices) {
    console.log(choices);
    if (choices.clockWidget == 0) {
        document.getElementById("TL").style.display = "none";
    }
    if (choices.weatherWidget == 0) {
        document.getElementById("TR").style.display = "none";
    }
    if (choices.mapWidget == 0) {
        document.getElementById("ML").style.display = "none";
    }
    if (choices.twitterWidget == 0) {
        document.getElementById("MR").style.display = "none";
    }
    if (choices.calendarWidget == 0) {
        document.getElementById("BL").style.display = "none";
        document.getElementById("BM").style.display = "none";
        document.getElementById("BR").style.display = "none";
        document.getElementById("titleEvent").style.display = "none";
    }

}
/*
 "calendarWidget": 1,
 "clockWidget": 1,
 "email": "dsundby1000@gmail.com",
 "facepath": "-",
 "homeAddress": "3415 nirmal ct",
 "mapWidget": 1,
 "name": "dedric sundby",
 "pin": "d404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db",
 "twitterWidget": 1,
 "weatherWidget": 1,
 "workAddress": "atlanta ga"
 */
/*function parseTime(startTime) {
 var time = startTime;
 var retro = "";

 for (i = 14; i > 9; i--) {
 retro = retro + (time.charAt(time.length - i));
 }
 /* if(retro.charAt(0)==0){
 retro=retro+"AM";
 } else{
 retro=retro+"PM"
 }

 return retro;
 }
 */