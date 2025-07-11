package com.example.taskschedule;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image; // Required for the icon
import javafx.stage.Stage;

import java.io.IOException;
import java.io.InputStream; // Required to load the icon resource
import java.net.URL;
import java.util.Locale;

public class MainApp extends Application {

    @Override
    public void start(Stage primaryStage) {
        System.out.println(">>>> Diagnostic Property: " + System.getProperty("my.diagnostic.property"));
        try {
            // This part remains the same, it's already well-written.
            URL fxmlLocation = getClass().getResource("/com/example/taskschedule/view/MainWindow.fxml");

            if (fxmlLocation == null) {
                System.err.println("Critical Error: Could not find 'MainWindow.fxml'.");
                // In a real application, you might show a user-friendly error dialog here.
                return;
            }

            Parent root = FXMLLoader.load(fxmlLocation);

            // --- START: ADDED CODE FOR THE ICON ---
            // Load the icon from the resources/images folder.
            // The path starts with "/" to indicate it's an absolute path from the root of the resources.
            try (InputStream iconStream = getClass().getResourceAsStream("/images/app-icon.png")) {
                if (iconStream != null) {
                    primaryStage.getIcons().add(new Image(iconStream));
                } else {
                    System.err.println("Warning: Application icon not found at /images/app-icon.png");
                }
            } catch (IOException e) {
                System.err.println("Error loading application icon.");
                e.printStackTrace();
            }
            // --- END: ADDED CODE FOR THE ICON ---

            // Set the title and show the stage as before.
            primaryStage.setTitle("Task Planner");
            primaryStage.setScene(new Scene(root, 1024, 768)); // A slightly larger default size
            primaryStage.show();

        } catch (IOException e) {
            System.err.println("An error occurred while loading the FXML view.");
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        // Set the default locale to US English to ensure the calendar is in English.
        Locale.setDefault(Locale.US);
        launch(args);
    }
}