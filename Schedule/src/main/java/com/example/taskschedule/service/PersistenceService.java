package com.example.taskschedule.service;

import com.example.taskschedule.model.RecurringTask;
import com.example.taskschedule.model.SchedulableItem;
import com.example.taskschedule.model.SimpleTask;
import com.example.taskschedule.util.LocalDateAdapter;
import com.example.taskschedule.util.RuntimeTypeAdapterFactory;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParseException;
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


    // In PersistenceService.java

    public List<SchedulableItem> loadTasks() {
        try (FileReader reader = new FileReader(SAVE_FILE_PATH)) {
            Type type = new TypeToken<ArrayList<SchedulableItem>>() {}.getType();
            List<SchedulableItem> loadedItems = gson.fromJson(reader, type);

            if (loadedItems == null) {
                logger.info("tasks.json file is empty. Starting with a new schedule.");
                return new ArrayList<>();
            }

            logger.info("Successfully loaded {} tasks from {}", loadedItems.size(), SAVE_FILE_PATH);
            return loadedItems;

            // --- SUGGESTION: Add this catch block ---
            // This handles cases where the file exists but is empty, corrupted, or in an old format.
        } catch (JsonParseException e) {
            logger.error("Failed to parse tasks.json. The file might be corrupted or in an old format. Starting with a new schedule.", e);
            return new ArrayList<>(); // Return an empty list to prevent a crash
        } catch (IOException e) {
            // This handles the case where the file doesn't exist at all.
            logger.warn("No save file found at {}. Starting with an empty schedule.", SAVE_FILE_PATH);
            return new ArrayList<>();
        }
    }
}