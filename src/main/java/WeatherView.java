import javafx.application.Application;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Created by La molybdenstar on 11/14/2016.
 */
public class WeatherView extends Application{
    

    public WeatherView() throws IOException {
    }

    @Override
    public void start(Stage primaryStage) throws Exception {

        W.getForecast();

    }
}
