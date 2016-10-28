
import com.google.api.client.util.DateTime;
import com.google.api.services.calendar.model.Event;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;


public class JUANMAIN extends Application{



    public static void main (String[] args) throws IOException {

        Weather w = new Weather();

        System.out.println(w.getTemp());
        System.out.println(w.getForecast());
        System.out.println(w.getLocation());

        Calendar cal = new Calendar();

        List<Event> events = cal.getEvents();

        if (events.size() == 0) {
            System.out.println("No upcoming events found.");
        } else {
            System.out.println("Upcoming events");

            for (Event event : events) {

                DateTime start = event.getStart().getDateTime();
                if (start == null) {
                    start = event.getStart().getDate();
                }
                System.out.printf("%s (%s)\n", event.getSummary(), start);
            }
        }

        Application.launch(JUANMAIN.class, (java.lang.String[])null);

    }


    @Override
    public void start(Stage primaryStage) {
        try {
            GridPane page =  (GridPane) FXMLLoader.load(JUANMAIN.class.getResource("Calendar.fxml"));
            Scene scene = new Scene(page);
            primaryStage.setScene(scene);
            primaryStage.setTitle("Calendar");
            primaryStage.show();
        } catch (Exception ex) {
            Logger.getLogger(JUANMAIN.class.getName()).log(Level.SEVERE, null, ex);
        }
    }




}