import com.sun.javafx.css.Style;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.*;
import javafx.scene.shape.Shape;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.awt.*;
import java.io.IOException;

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
<<<<<<< HEAD



=======
    
>>>>>>> origin/master

    public WeatherView() throws IOException {

    }

    @Override
    public void start(Stage primaryStage) throws Exception {

        Weather W = new Weather();
        BorderPane pane = new BorderPane();
        pane.setStyle("-fx-background: black;");
        ScrollPane scroll = new ScrollPane();
        pane.setCenter(scroll);
        scroll.setStyle("-fx-background-color: black;");


        Label label = new Label(W.getForecast()+"\n\n" + W.getLocation()+"\n\n"+ W.getTemp());
        label.setTextFill(Color.CYAN);
        label.setStyle("-fx-font-size: 25");
        scroll.setContent(label);

        Scene scene = new Scene(pane);

        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args){
        launch(args);
    }
}
