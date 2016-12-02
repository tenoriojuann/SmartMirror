import java.lang.reflect.Field;
import javafx.application.Application;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import org.w3c.dom.Document;

public class TestTranparentApps extends Application {

    @Override
    public void start(Stage mainstage) {
        WebView webview;
        webview = new WebView();
        WebEngine webviewEngine = webview.getEngine();

        webviewEngine.load(this.getClass().getResource("news.html").toExternalForm());

        Scene scene = new Scene(webview);
        scene.setFill(null);

        // Transparent

        final com.sun.webkit.WebPage webPage = com.sun.javafx.webkit.Accessor.getPageFor(webviewEngine);
        webPage.setBackgroundColor(0);

        mainstage.setScene(scene);
        mainstage.initStyle(StageStyle.TRANSPARENT);
        mainstage.setWidth(550);
        mainstage.setHeight(750);
        mainstage.setX(600);
        mainstage.setY(500);

        mainstage.show();
    }
}