package com.example.taskschedule.model;

import java.time.LocalDate;
import java.time.LocalTime;

/**
 * Represents a simple, non-recurring task that can be an all-day event
 * or have a specific start and end time.
 */
public class SimpleTask extends Task {

    private final LocalDate dueDate;
    private final LocalTime startTime; // Can be null for all-day tasks
    private final LocalTime endTime;   // Can be null for all-day tasks

    /**
     * Constructor for an all-day task.
     * @param description The task's description.
     * @param dueDate The date the task is due.
     */
    public SimpleTask(String description, LocalDate dueDate) {
        // Delegates to the main constructor with null times, indicating an all-day event.
        this(description, dueDate, null, null);
    }

    /**
     * Main constructor for a task that can be timed or all-day.
     * @param description The task's description.
     * @param dueDate The date the task is due.
     * @param startTime The specific start time (or null for all-day).
     * @param endTime The specific end time (or null for all-day).
     */
    public SimpleTask(String description, LocalDate dueDate, LocalTime startTime, LocalTime endTime) {
        // This super constructor call is based on your previous version of the Task class.
        // If your Task constructor is different, you may need to adjust this line.
        super(description, LocalDate.now(), false);

        this.dueDate = dueDate;
        this.startTime = startTime;
        this.endTime = endTime;
    }

    // --- Getters for the new fields ---

    public LocalDate getDueDate() {
        return dueDate;
    }

    public LocalTime getStartTime() {
        return startTime;
    }

    public LocalTime getEndTime() {
        return endTime;
    }

    /**
     * Checks if the task is an all-day event.
     * @return true if the task does not have a specific start or end time.
     */
    public boolean isAllDay() {
        return startTime == null || endTime == null;
    }

    // --- Other useful methods for the model ---

    @Override
    public boolean isDueToday() {
        return dueDate.equals(LocalDate.now());
    }

    public boolean isScheduledFor(LocalDate date) {
        return dueDate.equals(date);
    }

    @Override
    public String getDetails() {
        String status = isComplete() ? "Completed" : "Pending";
        if (isAllDay()) {
            return String.format("[Simple Task] %s - Due: %s (All Day) - Status: %s",
                    getDescription(), dueDate, status);
        } else {
            return String.format("[Simple Task] %s - Due: %s from %s to %s - Status: %s",
                    getDescription(), dueDate, startTime, endTime, status);
        }
    }
}