
import java.io.IOException;
import java.util.List;
import java.util.Locale;
import java.util.Timer;
import java.util.TimerTask;

import com.google.api.client.util.DateTime;
import com.google.api.services.calendar.model.Event;
import com.google.api.services.calendar.model.EventDateTime;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.geometry.Rectangle2D;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ListCell;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.Background;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

public class CalendarViewTest extends Application {


    Timer timer = new Timer ();

    public Image chooseIcon(String text){

        if(text.toLowerCase().contains("Cloud".toLowerCase())){
            return new Image(this.getClass().getResource("Clouds.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("rain".toLowerCase())){
            return new Image(this.getClass().getResource("Rain.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("snow".toLowerCase())){
            return new Image(this.getClass().getResource("Snow.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("Sun".toLowerCase()) || text.toLowerCase().contains("clear".toLowerCase())){
            return new Image(this.getClass().getResource("Sun.png").toExternalForm());
        }
        else if(text.toLowerCase().contains("heavy rain".toLowerCase())){
            return new Image(this.getClass().getResource("HeavyRainCloud.png").toExternalForm());
        }

        return null;

    }

    @Override
    public void start(Stage primaryStage) throws IOException {







        CalendarView calendarView = new CalendarView() ;

        BorderPane root = new BorderPane();
        root.setBottom(calendarView.getView());
        Scene scene = new Scene(root);
        primaryStage.setScene(scene);

        primaryStage.show();





        //
        //  WEATHER
        //
        Weather W = new Weather();
        BorderPane pane = new BorderPane();

        root.setLeft(pane);

        ImageView image = new ImageView();

        //pane.setBackground();
        pane.setTop(image);


        Text text ;

        Text clock =  new Text();
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



        scene.setFill(null);
        root.setStyle("-fx-background-color:black");

        // Transparent


    }

    public static void main(String[] args) throws IOException {

        launch(args);
    }
}