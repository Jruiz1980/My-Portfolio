package com.example.taskschedule.model;

/**
 * Interfaz que define el contrato para cualquier elemento que pueda ser
 * agendado.
 * Esto es una forma de ABSTRACCIÓN aún más flexible que una clase abstracta.
 */
public interface SchedulableItem {
    String getDetails();
    boolean isDueToday();
}