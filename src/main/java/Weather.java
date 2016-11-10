
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;

import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class Weather {


    //OPENWEATHER KEY
    private InputStream sc = this.getClass().getResourceAsStream("/key.json");

    private JsonParser parser = new JsonParser();
    private JsonObject JSON = (JsonObject) parser.parse(new InputStreamReader(
                                                                sc));

    private String lat,lng;



    private URL ipURL = new URL("http://ip-api.com/json");
    JsonObject data;
    JsonObject location;

    public Weather() throws IOException {
        Request();
        setLocation();
    }


    public void Request() throws IOException {


        HttpURLConnection requestLocation = (HttpURLConnection) ipURL.openConnection();
        requestLocation.connect();



        JsonElement root2 = parser.parse(new InputStreamReader((InputStream) requestLocation.getContent()));

        location = root2.getAsJsonObject();

        setLocation();

        URL url = new URL("http://api.openweathermap.org/data/2.5/forecast?lat="+lat+"&lon="+lng+"&units=imperial&appid="+JSON.get("WeatherAPIKey").getAsString());

        HttpURLConnection request = (HttpURLConnection) url.openConnection();
        request.connect();


        JsonElement root = parser.parse(new InputStreamReader((InputStream) request.getContent())); //Convert the input stream to a json element
        data = root.getAsJsonObject(); //May be an array, may be an object.

    }


    public void setLocation(){
        lat = location.get("lat").getAsString();
        lng = location.get("lon").getAsString();
    }

    public String getLocation(){

        return "Lat: " + lat + ", " + "lon: " + lng;
    }

    public String getTemp(){
        JsonObject main = data.get("list").getAsJsonArray().get(0).getAsJsonObject().get("main").getAsJsonObject();

        return main.get("temp").getAsString();
    }

    public String getForecast(){
        JsonObject weather = data.get("list").getAsJsonArray().get(0).getAsJsonObject().get("weather").getAsJsonArray().get(0).getAsJsonObject();

        return weather.get("description").getAsString();
    }
}
