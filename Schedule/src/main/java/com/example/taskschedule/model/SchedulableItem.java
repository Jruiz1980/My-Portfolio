package com.example.taskschedule.model;

import java.time.LocalDate;

/**
 * Represents an abstract item that can be scheduled.
 * This demonstrates ABSTRACTION and provides a base for INHERITANCE.
 */
public abstract class SchedulableItem {
    protected LocalDate date;
    protected String description;

    public SchedulableItem(LocalDate date, String description) {
        this.date = date;
        this.description = description;
    }

    public abstract String getDisplayDetails();

    // Getters and Setters
    public LocalDate getDate() { return date; }
    public String getDescription() { return description; }
}
