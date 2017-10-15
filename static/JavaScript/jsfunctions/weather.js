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

            curMinute = objToday.getMinutes() < 10 ? "0" + objToday.getMinutes(): objToday.getMinutes(),
            curSeconds = objToday.getSeconds() < 10 ? "0" + objToday.getSeconds() : objToday.getSeconds(),
            curMeridiem = objToday.getHours() > 12 ? "PM" : "AM";

        CurrentDate = dayOfWeek + " " + curMonth + " " + dayOfMonth + ", " + curYear;
        CurrentTime = curHour + ":" + curMinute + ":" + curSeconds + " " + curMeridiem;
        document.getElementById("date").innerHTML = CurrentDate;
        document.getElementById(id).innerHTML = CurrentTime;
        /*Uncomment for real-time clock*/
       // console.log(CurrentDate + "\n" + CurrentTime);
        setTimeout('date_time("'+id+'");','1000');
        return true;

}

var currentWeather= {
    temp:"temp",
    imageURL:"",
    description:"",
    location:""

}
function weatherData() {
    $.ajax({
        url: '/weather',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data);
            currentWeather.temp= data.main.temp;
            currentWeather.imageURL = data.weather[0].icon;
            currentWeather.description= data.weather[0].description;
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
function mapsData(){

}




