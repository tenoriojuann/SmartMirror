
import java.io.IOException;
import java.util.List;
import java.util.Locale;

import com.google.api.client.util.DateTime;
import com.google.api.services.calendar.model.Event;
import com.google.api.services.calendar.model.EventDateTime;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ListCell;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

public class CalendarViewTest extends Application {

    @Override
    public void start(Stage primaryStage) throws IOException {
        CalendarView calendarView = new CalendarView() ;

        BorderPane root = new BorderPane(calendarView.getView());
        Scene scene = new Scene(root);
        primaryStage.setScene(scene);
        scene.setFill(null);
        primaryStage.initStyle(StageStyle.TRANSPARENT);
        primaryStage.setX(0);
        primaryStage.setY(550);
        primaryStage.show();

    }

    public static void main(String[] args) throws IOException {

        launch(args);
    }
}