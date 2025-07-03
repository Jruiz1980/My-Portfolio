package com.example.taskschedule.model;

import java.time.LocalDate;

/**
 * A concrete class representing a task.
 * This demonstrates ENCAPSULATION (private fields, public methods)
 * and INHERITANCE (extends SchedulableItem).
 */
public class Task extends SchedulableItem {
    private boolean isCompleted;

    public Task(LocalDate date, String description) {
        super(date, description);
        this.isCompleted = false;
    }

    @Override
    public String getDisplayDetails() {
        return (isCompleted ? "[X] " : "[ ] ") + description;
    }

    public void setCompleted(boolean completed) { isCompleted = completed; }
    public boolean isCompleted() { return isCompleted; }
}

