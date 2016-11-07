
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Weather {

    private String key = "0542a8054137881685a1941c9de05d2a";

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

        JsonParser IP = new JsonParser();

        JsonElement root2 = IP.parse(new InputStreamReader((InputStream) requestLocation.getContent()));

        location = root2.getAsJsonObject();

        setLocation();

        URL url = new URL("http://api.openweathermap.org/data/2.5/forecast?lat="+lat+"&lon="+lng+"&units=imperial&appid="+key);

        HttpURLConnection request = (HttpURLConnection) url.openConnection();
        request.connect();

        JsonParser jp = new JsonParser(); //from gson
        JsonElement root = jp.parse(new InputStreamReader((InputStream) request.getContent())); //Convert the input stream to a json element
        data = root.getAsJsonObject(); //May be an array, may be an object.

    }


    public void setLocation(){
        lat = location.get("lat").toString();
        lng = location.get("lon").toString();
    }

    public String getLocation(){

        return "Lat: " + lat + ", " + "lon: " + lng;
    }

    public String getTemp(){
        JsonObject main = data.get("list").getAsJsonArray().get(0).getAsJsonObject().get("main").getAsJsonObject();

        return main.get("temp").toString();
    }

    public String getForecast(){
        JsonObject weather = data.get("list").getAsJsonArray().get(0).getAsJsonObject().get("weather").getAsJsonArray().get(0).getAsJsonObject();

        return weather.get("description").toString();
    }
}
