package com.example.taskschedule.view;

import com.example.taskschedule.model.RecurringTask;
import com.example.taskschedule.model.SimpleTask;
import com.example.taskschedule.model.Task;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;

public class TaskDialogController {

    private static final Logger logger = LoggerFactory.getLogger(TaskDialogController.class);

    // --- New FXML Fields ---
    @FXML private VBox simpleTaskPane;
    @FXML private VBox recurringTaskPane;
    @FXML private VBox timeFieldsPane;
    @FXML private CheckBox allDayCheckBox;
    @FXML private Spinner<Integer> startHourSpinner;
    @FXML private Spinner<Integer> startMinuteSpinner;
    @FXML private Spinner<Integer> endHourSpinner;
    @FXML private Spinner<Integer> endMinuteSpinner;

    // --- Existing FXML Fields ---
    @FXML private TextField descriptionField;
    @FXML private DatePicker datePicker;
    @FXML private CheckBox recurringCheckBox;
    @FXML private ComboBox<DayOfWeek> dayOfWeekComboBox;

    @FXML
    public void initialize() {
        // Configure recurring/simple task pane visibility
        recurringCheckBox.selectedProperty().addListener((obs, oldVal, isRecurring) -> {
            simpleTaskPane.setVisible(!isRecurring);
            recurringTaskPane.setVisible(isRecurring);
        });

        // Configure time fields visibility based on "All Day" checkbox
        allDayCheckBox.selectedProperty().addListener((obs, oldVal, isAllDay) -> {
            timeFieldsPane.setVisible(!isAllDay);
        });
        timeFieldsPane.setVisible(false); // Initially hidden because "All Day" is checked

        // Populate combo box
        dayOfWeekComboBox.getItems().setAll(DayOfWeek.values());
        datePicker.setValue(LocalDate.now());

        // Configure spinners for time selection
        setupTimeSpinners();
    }

    private void setupTimeSpinners() {
        // Value factories define the range and initial value for each spinner
        startHourSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 23, LocalTime.now().getHour()));
        startMinuteSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 59, 0));
        endHourSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 23, LocalTime.now().plusHours(1).getHour()));
        endMinuteSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 59, 0));

        // Make spinners editable for direct input
        startHourSpinner.setEditable(true);
        startMinuteSpinner.setEditable(true);
        endHourSpinner.setEditable(true);
        endMinuteSpinner.setEditable(true);
    }

    public void setTask(Task task) {
        descriptionField.setText(task.getDescription());
        if (task instanceof SimpleTask simpleTask) {
            recurringCheckBox.setSelected(false);
            datePicker.setValue(simpleTask.getDueDate());
            allDayCheckBox.setSelected(simpleTask.isAllDay());

            if (!simpleTask.isAllDay()) {
                startHourSpinner.getValueFactory().setValue(simpleTask.getStartTime().getHour());
                startMinuteSpinner.getValueFactory().setValue(simpleTask.getStartTime().getMinute());
                endHourSpinner.getValueFactory().setValue(simpleTask.getEndTime().getHour());
                endMinuteSpinner.getValueFactory().setValue(simpleTask.getEndTime().getMinute());
            }

        } else if (task instanceof RecurringTask recurringTask) {
            recurringCheckBox.setSelected(true);
            dayOfWeekComboBox.setValue(recurringTask.getRecurringDay());
        }
    }

    public Task processResults() {
        String description = descriptionField.getText();
        if (description == null || description.trim().isEmpty()) {
            showError("Description cannot be empty.");
            return null;
        }

        if (recurringCheckBox.isSelected()) {
            DayOfWeek day = dayOfWeekComboBox.getValue();
            if (day == null) {
                showError("Please select a day for the recurring task.");
                return null;
            }
            return new RecurringTask(description, day);
        } else {
            LocalDate date = datePicker.getValue();
            if (date == null) {
                showError("Please select a due date.");
                return null;
            }

            if (allDayCheckBox.isSelected()) {
                return new SimpleTask(description, date); // All-day task
            } else {
                // Timed task
                LocalTime startTime = LocalTime.of(startHourSpinner.getValue(), startMinuteSpinner.getValue());
                LocalTime endTime = LocalTime.of(endHourSpinner.getValue(), endMinuteSpinner.getValue());

                if (endTime.isBefore(startTime)) {
                    showError("End time cannot be before start time.");
                    return null;
                }
                return new SimpleTask(description, date, startTime, endTime);
            }
        }
    }

    private void showError(String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Validation Error");
        alert.setHeaderText(null);
        alert.setContentText(message);
        // ... (icon setting code remains the same)
        Stage stage = (Stage) alert.getDialogPane().getScene().getWindow();
        try (InputStream iconStream = getClass().getResourceAsStream("/images/app-icon.png")) {
            if (iconStream != null) {
                stage.getIcons().add(new Image(iconStream));
            }
        } catch (Exception e) {
            logger.error("Could not load dialog icon: {}", e.getMessage(), e);
        }
        alert.showAndWait();
    }
}