package com.example.taskschedule.model;

import java.time.LocalDate;

/**
 * Represents the abstract concept of a task.
 * This class provides the common properties and behaviors for all types of tasks,
 * such as SimpleTask and RecurringTask.
 * It cannot be instantiated directly.
 */
public abstract class Task implements SchedulableItem {

    // These fields are 'final' because they are set once in the constructor and should not change.
    private final String description;
    private final LocalDate creationDate;

    // This field can be changed, so it is not final.
    private boolean complete;

    /**
     * Base constructor for all task types. Subclasses will call this using super().
     * @param description The description of the task.
     * @param creationDate The date the task was created.
     * @param complete The initial completion status.
     */
    public Task(String description, LocalDate creationDate, boolean complete) {
        this.description = description;
        this.creationDate = creationDate;
        this.complete = complete;
    }

    // --- Getters and Setters ---

    public String getDescription() {
        return description;
    }

    public boolean isComplete() {
        return complete;
    }

    public void setComplete(boolean complete) {
        this.complete = complete;
    }

    public LocalDate getCreationDate() {
        return creationDate;
    }

    /**
     * Provides a default string representation for the task,
     * which is useful for displaying it in UI components like ListView.
     * @return The task's description.
     */
    @Override
    public String toString() {
        return this.description;
    }

    // --- Methods from SchedulableItem Interface ---

    /**
     * Provides a base implementation for getting task details.
     * Subclasses can override this to add more specific information.
     * @return A formatted string with the task's details.
     */
    @Override
    public String getDetails() {
        String status = complete ? "Completada" : "Pendiente";
        return String.format("Tarea: %s (%s)", description, status);
    }

    /**
     * This method is declared abstract because a generic 'Task' does not have a due date.
     * Each subclass (like SimpleTask) MUST provide its own specific implementation
     * to determine if it is due today.
     */
    @Override
    public abstract boolean isDueToday();
    public abstract boolean isScheduledFor(LocalDate date);
}