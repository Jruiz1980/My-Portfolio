package com.example.taskschedule.model;

import java.time.DayOfWeek;
import java.time.LocalDate;

/**
 * Represents a task that recurs on a specific day of the week.
 */
public class RecurringTask extends Task {

    private final DayOfWeek recurringDay;

    public RecurringTask(String description, DayOfWeek recurringDay) {
        // Call the parent constructor. A recurring task doesn't have a single creation date.
        super(description, LocalDate.now(), false);
        this.recurringDay = recurringDay;
    }

    public DayOfWeek getRecurringDay() {
        return recurringDay;
    }

    /**
     * This is the required method.
     * It checks if the given date falls on the task's recurring day of the week.
     * @param date The date to check.
     * @return true if the date's day of the week matches the recurring day.
     */
    @Override
    public boolean isScheduledFor(LocalDate date) {
        return date.getDayOfWeek() == this.recurringDay;
    }

    @Override
    public boolean isDueToday() {
        return isScheduledFor(LocalDate.now());
    }

    @Override
    public String getDetails() {
        return String.format("[Recurring Task] %s - Every %s - Status: %s",
                getDescription(),
                recurringDay.toString(),
                isComplete() ? "Completed" : "Pending");
    }
}