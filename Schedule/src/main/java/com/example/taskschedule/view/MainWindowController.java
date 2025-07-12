package com.example.taskschedule.view;

import com.calendarfx.model.Calendar;
import com.calendarfx.model.CalendarSource;
import com.calendarfx.model.Entry;
import com.calendarfx.view.CalendarView;
import com.example.taskschedule.model.RecurringTask;
import com.example.taskschedule.model.SimpleTask;
import com.example.taskschedule.model.Task;
import com.example.taskschedule.model.SchedulableItem;
import com.example.taskschedule.service.Scheduler;
import com.example.taskschedule.service.PersistenceService;
import javafx.stage.WindowEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class MainWindowController {

    private static final Logger logger = LoggerFactory.getLogger(MainWindowController.class);

    // --- SOLUTION: Create an instance of the Scheduler ---
    // This will hold the application's data.
    private final Scheduler scheduler = new Scheduler();
    private final PersistenceService persistenceService = new PersistenceService();


    @FXML
    private CalendarView calendarView;

    private Calendar<Object> myCalendar;

    @FXML
    public void initialize() {
        myCalendar = new Calendar<>("My Tasks");
        myCalendar.setStyle(Calendar.Style.STYLE4);

        CalendarSource myCalendarSource = new CalendarSource("Main");
        myCalendarSource.getCalendars().add(myCalendar);

        calendarView.getCalendarSources().add(myCalendarSource);

        loadTasksFromService();

        calendarView.sceneProperty().addListener((obs, oldScene, newScene) -> {
            if (newScene != null) {
                newScene.windowProperty().addListener((obs2, oldWindow, newWindow) -> {
                    if (newWindow != null) {
                        newWindow.addEventHandler(WindowEvent.WINDOW_CLOSE_REQUEST, event -> saveTasksToService());
                    }
                });
            }
        });
    }

    private void loadTasksFromService() {
        List<SchedulableItem> loadedItems = persistenceService.loadTasks();
        loadedItems.forEach(item -> {
            scheduler.addItem(item);
            if (item instanceof Task task) {
                myCalendar.addEntry(createEntryFromTask(task));
            }
        });
    }

    @FXML
    private void handleShowDueToday() {
        // 1. Get the data from the scheduler
        List<SchedulableItem> dueToday = scheduler.getItemsDueToday();

        // 2. Prepare the content for the dialog
        String contentText;
        if (dueToday.isEmpty()) {
            contentText = "You have no tasks due today. Great job!";
        } else {
            StringBuilder sb = new StringBuilder("Tasks due today:\n\n");
            dueToday.forEach(item -> sb.append("• ").append(item.getDetails()).append("\n"));
            contentText = sb.toString();
        }

        // 3. Show the information to the user
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Today's Tasks");
        alert.setHeaderText(null);
        alert.setContentText(contentText);
        setIconForDialog(alert); // Reuse your helper to set the icon
        alert.showAndWait();
    }

    private void saveTasksToService() {
        // The scheduler holds the "source of truth" for our data
        persistenceService.saveTasks(scheduler.getAllItems()); // You'll need to add getAllItems() to Scheduler
    }

    /**
     * Handles creating a new task by showing a dialog.
     */
    @FXML
    private void handleAddNewTask() {
        showTaskDialog(null).ifPresent(task -> {
            // --- SOLUTION: Add the new task to the scheduler first ---
            scheduler.addItem(task);

            // Then, create the visual entry for the calendar
            Entry<?> newEntry = createEntryFromTask(task);
            myCalendar.addEntry(newEntry);

            // You can optionally print to the console to verify
            scheduler.showAllItems();
        });
    }

    /**
     * Handles editing a selected task by showing a pre-populated dialog.
     * This method is ready to be wired to a UI button in MainWindow.fxml.
     */
    @FXML
    private void handleEditTask() {
        Entry<?> selectedEntry = calendarView.getSelections().stream().findFirst().orElse(null);

        if (selectedEntry != null && selectedEntry.getUserObject() instanceof Task taskToEdit) {
            @SuppressWarnings("unchecked")
            Entry<Object> entryToUpdate = (Entry<Object>) selectedEntry;

            // Show the dialog pre-populated with the task's data
            showTaskDialog(taskToEdit).ifPresent(updatedTask -> {
                // --- SOLUTION: Update the data in the scheduler ---
                // Remove the old task object and add the new one.
                scheduler.removeItem(taskToEdit);
                scheduler.addItem(updatedTask);

                // Then, update the visual entry on the calendar
                updateEntryFromTask(entryToUpdate, updatedTask);

                // You can optionally print to the console to verify
                scheduler.showAllItems();
            });
        } else {
            showInfoDialog("Please select a task to edit.");
        }
    }

    /**
     * Handles deleting one or more selected tasks after confirmation.
     */
    @FXML
    private void handleDeleteTask() {
        List<Entry<?>> selectedEntries = new ArrayList<>(calendarView.getSelections());

        if (selectedEntries.isEmpty()) {
            showInfoDialog("Please select a task to delete.");
            return;
        }

        Alert confirmation = new Alert(
                Alert.AlertType.CONFIRMATION,
                "Are you sure you want to delete the selected task(s)?",
                ButtonType.YES, ButtonType.NO
        );
        setIconForDialog(confirmation);

        confirmation.showAndWait().ifPresent(response -> {
            if (response == ButtonType.YES) {
                selectedEntries.forEach(entry -> {
                    // --- SOLUTION: Remove the task from the scheduler ---
                    if (entry.getUserObject() instanceof SchedulableItem itemToRemove) {
                        scheduler.removeItem(itemToRemove);
                    }

                    // Then, remove the visual entry from the calendar
                    if (entry.getCalendar() != null) {
                        myCalendar.removeEntry(entry);
                    }
                });
                // You can optionally print to the console to verify
                scheduler.showAllItems();
            }
        });
    }

    /**
     * Shows the "About" dialog for the application.
     */
    @FXML
    private void handleAboutAction() {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("About Task Schedule");
        alert.setHeaderText("Task Schedule Application v1.0");
        alert.setContentText("""
                This application was created using JavaFX and CalendarFX.
                
                Developed by: Johnathan I. Ruiz
                Portfolio Project - 2025""");
        setIconForDialog(alert);
        alert.showAndWait();
    }

    // --- Refactored Business Logic and Helper Methods ---

    /**
     * A centralized method to show the task dialog for both creating and editing tasks.
     *
     * @param taskToEdit The task to edit, or null if creating a new task.
     * @return An Optional containing the created/updated Task, or empty if canceled.
     */
    private Optional<Task> showTaskDialog(Task taskToEdit) {
        try {
            Dialog<Task> dialog = new Dialog<>();
            dialog.setTitle(taskToEdit == null ? "New Task" : "Edit Task");
            dialog.setHeaderText(taskToEdit == null ? "Enter the details for the new task." : "Edit the task details.");
            setIconForDialog(dialog);

            FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("/com/example/taskschedule/view/TaskDialog.fxml"));
            dialog.getDialogPane().setContent(fxmlLoader.load());

            TaskDialogController controller = fxmlLoader.getController();
            if (taskToEdit != null) {
                controller.setTask(taskToEdit); // Pre-populate the dialog for editing
            }

            ButtonType acceptButtonType = new ButtonType("Accept", ButtonBar.ButtonData.OK_DONE);
            dialog.getDialogPane().getButtonTypes().addAll(acceptButtonType, ButtonType.CANCEL);

            dialog.setResultConverter(dialogButton ->
                    dialogButton == acceptButtonType ? controller.processResults() : null);

            return dialog.showAndWait();

        } catch (IOException e) {
            logger.error("Failed to load task dialog FXML.", e);
            showErrorDialog();
            return Optional.empty();
        }
    }

    /**
     * Converts a custom Task object into a new CalendarFX Entry object.
     */
    private Entry<?> createEntryFromTask(Task task) {
        Entry<Object> entry = new Entry<>(task.getDescription());
        updateEntryFromTask(entry, task); // Reuse update logic
        return entry;
    }

    /**
     * Updates an existing CalendarFX Entry with data from a Task object.
     */
    private void updateEntryFromTask(Entry<Object> entry, Task task) {
        entry.setTitle(task.getDescription());
        entry.setUserObject(task);
        entry.setRecurrenceRule(null); // Clear any previous recurrence rule

        if (task instanceof SimpleTask simpleTask) {
            if (simpleTask.isAllDay()) {
                // It's an all-day task
                entry.setFullDay(true);
                entry.setInterval(simpleTask.getDueDate());
            } else {
                // It's a timed task
                entry.setFullDay(false);
                entry.setInterval(simpleTask.getDueDate(), simpleTask.getStartTime(), simpleTask.getDueDate(), simpleTask.getEndTime());
            }
        } else if (task instanceof RecurringTask recurringTask) {
            // Recurring task logic remains the same (all-day by default)
            entry.setFullDay(true);
            LocalDate today = LocalDate.now();
            LocalDate nextOccurrence = today.with(recurringTask.getRecurringDay());
            if (nextOccurrence.isBefore(today)) {
                nextOccurrence = nextOccurrence.plusWeeks(1);
            }
            entry.setInterval(nextOccurrence);

            String dayAbbreviation = recurringTask.getRecurringDay().toString().substring(0, 2);
            String rrule = String.format("FREQ=WEEKLY;BYDAY=%s", dayAbbreviation);
            entry.setRecurrenceRule(rrule);
        }
    }

    // --- Dialog Helper Methods ---

    private void showErrorDialog() {
        Alert alert = new Alert(Alert.AlertType.ERROR, "Could not open the task dialog window.");
        alert.setTitle("Application Error");
        alert.setHeaderText(null);
        setIconForDialog(alert);
        alert.showAndWait();
    }

    private void showInfoDialog(String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION, message);
        alert.setTitle("No Selection");
        alert.setHeaderText(null);
        setIconForDialog(alert);
        alert.showAndWait();
    }


    private void setIconForDialog(Dialog<?> dialog) {
        Stage stage = (Stage) dialog.getDialogPane().getScene().getWindow();
        try (InputStream iconStream = getClass().getResourceAsStream("/images/app-icon.png")) {
            if (iconStream != null) {
                stage.getIcons().add(new Image(iconStream));
            }
        } catch (Exception e) {
            logger.error("Could not load dialog icon.", e);
        }
    }
}