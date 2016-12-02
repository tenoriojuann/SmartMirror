import com.sun.javafx.css.Style;
import javafx.application.Application;
import javafx.event.Event;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.IOException;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.EventListener;
import java.util.Timer;
import java.util.TimerTask;

/**
 * Created by La molybdenstar on 11/14/2016.
 *
 * # MagicMirror

 This is a JAVA project built with GRADLE and at the end it creates an executable JAR file.

 There are two widgets in this JAVAFX application, one displays the weather and the other displays a calendar
 with all the information pulled from your Google account.

 Since Google requires us to build the project with GRADLE to be able to pull the events from the Google calendar we had no option there.
 The authentication works by sing OAuth2. This way we are to bounded to hard-coding the username and passwords. Rather we let the user login by using a browser and then it gets a token which is used to login to the user's account.

 To pull the weather information we simply rewrote the Python script that we had for one of the assignments into Java and JavaFX.
 */
public class WeatherView extends Application{


    Timer timer = new Timer ();

    public WeatherView() throws IOException {

    }

    public Image chooseIcon(String text){

        if(text.toLowerCase().contains("Cloud".toLowerCase())){
            return new Image(this.getClass().getResource("/Icons/Clouds.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("rain".toLowerCase())){
            return new Image(this.getClass().getResource("/Icons/rain.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("snow".toLowerCase())){
            return new Image(this.getClass().getResource("/Icons/Snow.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("Sun".toLowerCase()) || text.toLowerCase().contains("clear".toLowerCase())){
            return new Image(this.getClass().getResource("/Icons/Sun.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("heavy rain".toLowerCase())){
            return new Image(this.getClass().getResource("/Icons/HeavyRain.png").toExternalForm());
        }

        return null;

    }

    @Override
    public void start(Stage primaryStage) throws Exception {

        Weather W = new Weather();
        BorderPane pane = new BorderPane();
        ImageView image = new ImageView();

        //pane.setBackground();
        pane.setCenter(image);


        Text text ;


        text = new Text(W.getForecast());

        text.setFill(Color.CYAN);
        text.setStyle("-fx-font-size: 50pt ;");
        pane.setBottom(text);

        image.setImage(chooseIcon(text.getText()));


        TimerTask hourlyTask = new TimerTask () {
            @Override
            public void run () {
                text.setText(W.getForecast());
            }
        };

        // schedule the task to run starting now and then every hour...
        timer.schedule (hourlyTask, 0l, 1000*60*30);



        // Action Listener, listening for changes in the text

        text.textProperty().addListener((observable, oldValue, newValue) -> {
            image.setImage(chooseIcon(newValue));
        });


        Scene scene = new Scene(pane);


        // Transparent
        scene.setFill(null);
        primaryStage.initStyle(StageStyle.TRANSPARENT);
        // Transparent


        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args){
        launch(args);
    }
}
