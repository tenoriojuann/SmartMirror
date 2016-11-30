/**
 * Created by Tenor on 11/30/2016.
 */

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class Map extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {

        WebView webview = new WebView();
        WebEngine engine = webview.getEngine();
        engine.load(this.getClass().getResource("page.html").toExternalForm());
        webview.getEngine().setJavaScriptEnabled(true);
        primaryStage.setScene(new Scene(webview));
        primaryStage.show();
    }
}
