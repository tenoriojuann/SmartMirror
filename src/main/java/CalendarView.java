import java.io.IOException;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.time.format.TextStyle;
import java.time.temporal.ChronoUnit;
import java.time.temporal.WeekFields;
import java.util.List;
import java.util.Locale;
import com.google.api.services.calendar.model.Event;
import javafx.beans.binding.Bindings;
import javafx.beans.property.ObjectProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.css.PseudoClass;
import javafx.geometry.HPos;
import javafx.scene.Node;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;

public class CalendarView {
    private final ObjectProperty<YearMonth> month = new SimpleObjectProperty<>();

    private final ObjectProperty<Locale> locale = new SimpleObjectProperty<>(Locale.getDefault());

    private final BorderPane view;
    private final GridPane calendar;

    private Calendar googleCal = new Calendar();


    public CalendarView(YearMonth month) {
        view = new BorderPane();
        view.getStyleClass().add("calendar");
        calendar = new GridPane();
        calendar.getStyleClass().add("calendar-grid");

        Label header = new Label();
        header.setMaxWidth(Double.MAX_VALUE);
        header.getStyleClass().add("calendar-header");

        this.month.addListener((obs, oldMonth, newMonth) -> {
            try {
                rebuildCalendar();
            } catch (IOException e) {
                e.printStackTrace();
            }
        });

        view.setTop(header);
        view.setCenter(calendar);

        view.getStylesheets().add(getClass().getResource("calendar.css").toExternalForm());

        setMonth(month);

        header.textProperty().bind(Bindings.createStringBinding(() ->
                        this.month.get().format(DateTimeFormatter.ofPattern("MMMM yyyy", locale.get())),
                this.month, this.locale));
    }

    public CalendarView() {
        this(YearMonth.now());
    }


    private void rebuildCalendar() throws IOException {

        calendar.getChildren().clear();

        WeekFields weekFields = WeekFields.of(locale.get());

        LocalDate first = month.get().atDay(1);

        int dayOfWeekOfFirst = first.get(weekFields.dayOfWeek());

        // column headers:
        for (int dayOfWeek = 1; dayOfWeek <= 7; dayOfWeek++) {
            LocalDate date = first.minusDays(dayOfWeekOfFirst - dayOfWeek);
            DayOfWeek day = date.getDayOfWeek();
            Label label = new Label(day.getDisplayName(TextStyle.SHORT_STANDALONE, locale.get()));
            label.getStyleClass().add("calendar-day-header");
            GridPane.setHalignment(label, HPos.CENTER);
            calendar.add(label, dayOfWeek - 1, 0);


        }

        LocalDate firstDisplayedDate = first.minusDays(dayOfWeekOfFirst - 1);
        LocalDate last = month.get().atEndOfMonth();
        int dayOfWeekOfLast = last.get(weekFields.dayOfWeek());
        LocalDate lastDisplayedDate = last.plusDays(7 - dayOfWeekOfLast);

        PseudoClass beforeMonth = PseudoClass.getPseudoClass("before-display-month");
        PseudoClass afterMonth = PseudoClass.getPseudoClass("after-display-month");


        List<Event> items = googleCal.getEvents();

        for (LocalDate date = firstDisplayedDate; !date.isAfter(lastDisplayedDate); date = date.plusDays(1)) {
            Label label = new Label(String.valueOf(date.getDayOfMonth()));
            label.getStyleClass().add("calendar-cell");
            label.pseudoClassStateChanged(beforeMonth, date.isBefore(first));
            label.pseudoClassStateChanged(afterMonth, date.isAfter(last));

            GridPane.setHalignment(label, HPos.CENTER);

            int dayOfWeek = date.get(weekFields.dayOfWeek());
            int daysSinceFirstDisplayed = (int) firstDisplayedDate.until(date, ChronoUnit.DAYS);
            int weeksSinceFirstDisplayed = daysSinceFirstDisplayed / 7;

            calendar.add(label, dayOfWeek - 1, weeksSinceFirstDisplayed + 1);


            for(Event item : items){
                String start = item.getStart().getDateTime().toStringRfc3339();
                if (start == null) {
                    start = (item.getStart().getDate().toStringRfc3339());
                }
                start = (start.charAt(8)+""+start.charAt(9));

                if ( Integer.parseInt(start) == date.getDayOfMonth()){
                    calendar.add(new Label("\n"+item.getSummary() ),dayOfWeek-1,weeksSinceFirstDisplayed+1);
                }
            }

        }
    }

    public Node getView() {
        return view;
    }

    public final ObjectProperty<YearMonth> monthProperty() {
        return this.month;
    }


    public final void setMonth(final YearMonth month) {
        this.monthProperty().set(month);
    }

    public final ObjectProperty<Locale> localeProperty() {
        return this.locale;
    }
}
