/**
 * Created by Dedric on 10/8/2017.
 */
var currentWeather= {
    temp:"temp",
    imageURL:"",
    description:"",
    location:""
}
function test() {
    $.ajax({
        url: '/weather',
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data);
            currentWeather.temp=data.main.temp;
            currentWeather.imageURL = data.weather[0].icon;
            currentWeather.description= data.weather[0].description;
            currentWeather.location = data.name;
            console.log(currentWeather);
        }
    });
}
