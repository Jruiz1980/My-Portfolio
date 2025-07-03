plugins {
    // Apply the application plugin to add support for building a CLI application in Java.
    application
    // Apply the JavaFX plugin
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    // Use Maven Central for resolving dependencies.
    mavenCentral()
}

javafx {
    version = "21" // The version of JavaFX you want to use
    modules("javafx.controls", "javafx.fxml") // The JavaFX modules your project needs
}

application {
    // Define the main class for the application.
    mainClass.set("TaskSchedule")
}

dependencies {
    // Use JUnit Jupiter for testing.
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
}

