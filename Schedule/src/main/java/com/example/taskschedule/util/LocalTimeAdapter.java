package com.example.taskschedule.util;

import com.google.gson.TypeAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonToken;
import com.google.gson.stream.JsonWriter;

import java.io.IOException;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

/**
 * Teaches Gson how to convert LocalTime objects to and from a JSON string.
 * It uses the standard ISO-8601 format (e.g., "14:30:00").
 */
public class LocalTimeAdapter extends TypeAdapter<LocalTime> {

    // Using a standard formatter ensures consistency and is a best practice.
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ISO_LOCAL_TIME;

    @Override
    public void write(JsonWriter out, LocalTime value) throws IOException {
        if (value == null) {
            out.nullValue();
        } else {
            out.value(value.format(FORMATTER));
        }
    }

    @Override
    public LocalTime read(JsonReader in) throws IOException {
        if (in.peek() == JsonToken.NULL) {
            in.nextNull();
            return null;
        }
        return LocalTime.parse(in.nextString(), FORMATTER);
    }
}