
import java.io.IOException;
import java.util.List;
import java.util.Locale;

import com.google.api.client.util.DateTime;
import com.google.api.services.calendar.model.Event;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ListCell;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

public class CalendarViewTest extends Application {

    @Override
    public void start(Stage primaryStage) {
        CalendarView calendarView = new CalendarView() ;

        Button next = new Button(">");
        next.setOnAction(e -> calendarView.nextMonth());

        Button previous = new Button("<");
        previous.setOnAction(e -> calendarView.previousMonth());

        ComboBox<Locale> localeCombo = new ComboBox<>();
        localeCombo.getItems().addAll(Locale.getAvailableLocales());
        localeCombo.setValue(Locale.getDefault());

        localeCombo.setCellFactory(lv -> new LocaleCell());
        localeCombo.setButtonCell(new LocaleCell());

        calendarView.localeProperty().bind(localeCombo.valueProperty());

        BorderPane.setAlignment(localeCombo, Pos.CENTER);
        BorderPane.setMargin(localeCombo, new Insets(10));

        BorderPane root = new BorderPane(calendarView.getView(), localeCombo, next, null, previous);
        Scene scene = new Scene(root);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static class LocaleCell extends ListCell<Locale> {
        @Override
        public void updateItem(Locale locale, boolean empty) {
            super.updateItem(locale, empty);
            setText(locale == null ? null : locale.getDisplayName(locale));
        }
    }

    public static void main(String[] args) throws IOException {

        Calendar googleCalendar = new Calendar();

        List<Event> items = googleCalendar.getEvents();

        if (items.size() == 0) {
            System.out.println("No upcoming events found.");
        } else {
            System.out.println("Upcoming events");
            for (Event event : items) {
                DateTime start = event.getStart().getDateTime();
                if (start == null) {
                    start = event.getStart().getDate();
                }
                System.out.printf("%s (%s)\n", event.getSummary(), start);
            }
        }
        launch(args);
    }
}