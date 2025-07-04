package com.example.taskschedule.view;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.ListView;

//import java.time.LocalDate;

public class MainWindowController {

    @FXML
    private ListView<String> taskListView;

    @FXML
    public void initialize() {
        // This is where you will load and display tasks.
        // Example of POLYMORPHISM could be a list of SchedulableItem.
        ObservableList<String> tasks = FXCollections.observableArrayList("Task 1", "Task 2", "Appointment 1");
        taskListView.setItems(tasks);
    }
}
