package com.example.taskschedule;

//import com.example.taskschedule.controller.MainWindowController;
import com.example.taskschedule.service.PersistenceService;
import com.example.taskschedule.service.Scheduler;
import com.example.taskschedule.view.MainWindowController;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Locale;

public class MainApp extends Application {

    private static final Logger logger = LoggerFactory.getLogger(MainApp.class);
    private static final String MAIN_WINDOW_FXML = "/com/example/taskschedule/view/MainWindow.fxml";
    private static final String APP_ICON_PATH = "/images/app-icon.png";

    private PersistenceService persistenceService;
    private Scheduler scheduler;

    /**
     * This method runs before start(). It's the perfect place to set up services.
     */
    @Override
    public void init() {
        logger.info("Initializing application services...");
        this.persistenceService = new PersistenceService();
        this.scheduler = new Scheduler();

        // Load tasks from disk into the scheduler
        //scheduler.setItems(persistenceService.loadTasks());
        logger.info("Application services initialized.");
    }

    @Override
    public void start(Stage primaryStage) {
        logger.info("Starting JavaFX application UI...");
        try {
            URL fxmlLocation = getClass().getResource(MAIN_WINDOW_FXML);
            if (fxmlLocation == null) {
                logger.error("Critical Error: FXML file not found at {}", MAIN_WINDOW_FXML);
                return;
            }

            FXMLLoader loader = new FXMLLoader(fxmlLocation);

            // This is the crucial part of your architecture: injecting the scheduler.
            //MainWindowController controller = new MainWindowController(scheduler);
            //loader.setController(controller);

            Scene scene = new Scene(loader.load(), 1024, 768); // Use the new, larger size

            // --- MERGED: Load the application icon ---
            loadApplicationIcon(primaryStage);

            // Use the new title
            primaryStage.setTitle("Task Planner");
            primaryStage.setScene(scene);
            primaryStage.show();

        } catch (IOException e) {
            logger.error("Failed to load the main application window.", e);
        }
    }

    /**
     * This method is called when the application is closed.
     * It's the perfect place to save all data.
     */
    @Override
    public void stop() {
        logger.info("Application is closing. Saving tasks...");
        if (persistenceService != null && scheduler != null) {
            persistenceService.saveTasks(scheduler.getAllItems());
            logger.info("Tasks saved successfully.");
        }
    }

    /**
     * Helper method to load the application icon from resources.
     * This improves code clarity by separating the logic from the start() method.
     */
    private void loadApplicationIcon(Stage stage) {
        try (InputStream iconStream = getClass().getResourceAsStream(APP_ICON_PATH)) {
            if (iconStream != null) {
                stage.getIcons().add(new Image(iconStream));
                logger.info("Application icon loaded successfully.");
            } else {
                logger.warn("Application icon not found at {}", APP_ICON_PATH);
            }
        } catch (IOException e) {
            logger.error("Error loading application icon.", e);
        }
    }

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        launch(args);
    }
}