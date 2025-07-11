package com.example.taskschedule.util;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;
import com.google.gson.TypeAdapter;
import com.google.gson.TypeAdapterFactory;
import com.google.gson.reflect.TypeToken;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;

import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * A helper for Gson that handles polymorphism by reading and writing a 'type' field.
 * This allows Gson to know which concrete class (e.g., SimpleTask, RecurringTask)
 * to instantiate when it encounters an interface (e.g., SchedulableItem).
 *
 * This is a well-known utility for Gson, adapted for this project.
 */
public final class RuntimeTypeAdapterFactory<T> implements TypeAdapterFactory {
    private final Class<?> baseType;
    private final String typeFieldName;
    private final Map<String, Class<?>> labelToSubtype = new LinkedHashMap<>();
    private final Map<Class<?>, String> subtypeToLabel = new LinkedHashMap<>();

    private RuntimeTypeAdapterFactory(Class<?> baseType, String typeFieldName) {
        if (typeFieldName == null || baseType == null) {
            throw new NullPointerException();
        }
        this.baseType = baseType;
        this.typeFieldName = typeFieldName;
    }

    public static <T> RuntimeTypeAdapterFactory<T> of(Class<T> baseType, String typeFieldName) {
        return new RuntimeTypeAdapterFactory<>(baseType, typeFieldName);
    }

    public RuntimeTypeAdapterFactory<T> registerSubtype(Class<? extends T> subtype, String label) {
        if (subtype == null || label == null) {
            throw new NullPointerException();
        }
        if (subtypeToLabel.containsKey(subtype) || labelToSubtype.containsKey(label)) {
            throw new IllegalArgumentException("types and labels must be unique");
        }
        labelToSubtype.put(label, subtype);
        subtypeToLabel.put(subtype, label);
        return this;
    }

    public <R> TypeAdapter<R> create(Gson gson, TypeToken<R> type) {
        if (type.getRawType() != baseType) {
            return null;
        }

        final Map<String, TypeAdapter<?>> labelToDelegate = new LinkedHashMap<>();
        final Map<Class<?>, TypeAdapter<?>> subtypeToDelegate = new LinkedHashMap<>();
        for (Map.Entry<String, Class<?>> entry : labelToSubtype.entrySet()) {
            TypeAdapter<?> delegate = gson.getAdapter(TypeToken.get(entry.getValue()));
            labelToDelegate.put(entry.getKey(), delegate);
            subtypeToDelegate.put(entry.getValue(), delegate);
        }

        return new TypeAdapter<R>() {
            @Override
            public R read(JsonReader in) throws IOException {
                JsonElement jsonElement = gson.getAdapter(JsonElement.class).read(in);
                JsonElement labelJsonElement = jsonElement.getAsJsonObject().remove(typeFieldName);
                if (labelJsonElement == null) {
                    throw new JsonParseException("cannot deserialize " + baseType
                            + " because it does not define a field named " + typeFieldName);
                }
                String label = labelJsonElement.getAsString();
                @SuppressWarnings("unchecked") // registration requires that subtype extends T
                TypeAdapter<R> delegate = (TypeAdapter<R>) labelToDelegate.get(label);
                if (delegate == null) {
                    throw new JsonParseException("cannot deserialize " + baseType + " subtype named "
                            + label + "; did you forget to register a subtype?");
                }
                return delegate.fromJsonTree(jsonElement);
            }

            @Override
            public void write(JsonWriter out, R value) throws IOException {
                Class<?> srcType = value.getClass();
                String label = subtypeToLabel.get(srcType);
                @SuppressWarnings("unchecked") // registration requires that subtype extends T
                TypeAdapter<R> delegate = (TypeAdapter<R>) subtypeToDelegate.get(srcType);
                if (delegate == null) {
                    throw new JsonParseException("cannot serialize " + srcType.getName()
                            + "; did you forget to register a subtype?");
                }
                JsonObject jsonObject = delegate.toJsonTree(value).getAsJsonObject();
                if (jsonObject.has(typeFieldName)) {
                    throw new JsonParseException("cannot serialize " + srcType.getName()
                            + " because it already defines a field named " + typeFieldName);
                }
                JsonObject clone = new JsonObject();
                clone.add(typeFieldName, new JsonPrimitive(label));
                for (Map.Entry<String, JsonElement> e : jsonObject.entrySet()) {
                    clone.add(e.getKey(), e.getValue());
                }
                gson.getAdapter(JsonElement.class).write(out, clone);
            }
        }.nullSafe();
    }
}