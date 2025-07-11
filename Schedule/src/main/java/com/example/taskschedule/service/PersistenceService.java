package com.example.taskschedule.service;

import com.example.taskschedule.model.RecurringTask;
import com.example.taskschedule.model.SchedulableItem;
import com.example.taskschedule.model.SimpleTask;
import com.example.taskschedule.util.LocalDateAdapter;
import com.example.taskschedule.util.RuntimeTypeAdapterFactory;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class PersistenceService {

    private static final Logger logger = LoggerFactory.getLogger(PersistenceService.class);
    private static final String SAVE_FILE_PATH = "tasks.json";
    private final Gson gson;

    public PersistenceService() {
        // This factory teaches Gson how to handle the SchedulableItem interface
        RuntimeTypeAdapterFactory<SchedulableItem> adapterFactory = RuntimeTypeAdapterFactory
                .of(SchedulableItem.class, "type")
                .registerSubtype(SimpleTask.class, "simple")
                .registerSubtype(RecurringTask.class, "recurring");

        // Here is the "usage" of your LocalDateAdapter!
        this.gson = new GsonBuilder()
                .registerTypeAdapter(LocalDate.class, new LocalDateAdapter())
                .registerTypeAdapterFactory(adapterFactory)
                .setPrettyPrinting()
                .create();
    }

    public void saveTasks(List<SchedulableItem> items) {
        try (FileWriter writer = new FileWriter(SAVE_FILE_PATH)) {
            gson.toJson(items, writer);
            logger.info("Successfully saved {} tasks to {}", items.size(), SAVE_FILE_PATH);
        } catch (IOException e) {
            logger.error("Failed to save tasks to file.", e);
        }
    }


    public List<SchedulableItem> loadTasks() {
        try (FileReader reader = new FileReader(SAVE_FILE_PATH)) {
            Type type = new TypeToken<ArrayList<SchedulableItem>>() {}.getType();
            List<SchedulableItem> loadedItems = gson.fromJson(reader, type);

            // --- SOLUTION: Add a null check for robustness ---
            // If the file was empty or contained "null", gson.fromJson returns null.
            // We should return an empty list instead to prevent NullPointerExceptions.
            if (loadedItems == null) {
                return new ArrayList<>();
            }

            logger.info("Successfully loaded {} tasks from {}", loadedItems.size(), SAVE_FILE_PATH);
            return loadedItems;

        } catch (IOException e) {
            logger.warn("No save file found or failed to read file. Starting with an empty schedule.");
            return new ArrayList<>(); // This is correct: return an empty list if the file doesn't exist.
        }
    }
}