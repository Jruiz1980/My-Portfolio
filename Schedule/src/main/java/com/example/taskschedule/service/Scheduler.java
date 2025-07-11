package com.example.taskschedule.service;

import com.example.taskschedule.model.SchedulableItem;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collector;
import java.util.stream.Collectors;

/**
 * Manages a collection of SchedulableItem.
 * Demonstrates POLYMORPHISM: the 'items' list can hold any object
 * that implements SchedulableItem (Task, SimpleTask, RecurringTask, etc.).
 */
public class Scheduler {
    // The list can hold any type of SchedulableItem.
    // Making it 'final' is a good practice as the list itself is never replaced.
    private final List<SchedulableItem> items = new ArrayList<>();

    public void addItem(SchedulableItem item) {
        this.items.add(item);
    }

    /**
     * Removes a specific item from the scheduler.
     * This is essential for handling deletions and edits.
     * @param item The item to remove.
     */
    public void removeItem(SchedulableItem item) {
        this.items.remove(item);
    }

    public List<SchedulableItem> getAllItems() {
        return Collections.unmodifiableList(items);
    }

    public void showAllItems() {
        System.out.println("--- All Scheduled Items ---");
        // Polymorphism in action: item.getDetails() calls the
        // correct method based on the object's actual type.
        for (SchedulableItem item : items) {
            System.out.println(item.getDetails());
        }
    }

    public List<SchedulableItem> getItemsDueToday() {
        return items.stream()
                .filter(SchedulableItem::isDueToday) // Polymorphism here as well
                .collect(Collectors.toList());
    }
}