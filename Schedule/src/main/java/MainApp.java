package com.example.taskschedule;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class MainApp extends Application {

    @Override
    public void start(Stage primaryStage) throws IOException {
        // Load the FXML file for the main window.
        // Note the path starts from the 'resources' folder.
        FXMLLoader loader = new FXMLLoader(getClass().getResource("view/MainWindow.fxml"));
        Parent root = loader.load();

        primaryStage.setTitle("My Task Schedule");
        primaryStage.setScene(new Scene(root, 800, 600));
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
