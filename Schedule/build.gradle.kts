plugins {
    // Use the standard 'id' notation for clarity and consistency
    id("application")
    id("org.openjfx.javafxplugin") version "0.1.0"
}

group = "com.example.taskschedule"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

application {
    // Define the main class for the application
    mainClass.set("com.example.taskschedule.MainApp")
}

javafx {
    // The version of JavaFX to use, compatible with your JDK
    version = "21.0.7"
    // The JavaFX modules your project needs
    modules("javafx.controls", "javafx.fxml")
}

dependencies {
    // JUnit 5 for testing
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")

    // Application dependencies
    implementation("com.calendarfx:view:11.12.5")
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("org.slf4j:slf4j-simple:2.0.12")
}

tasks.named<JavaExec>("run") {
    // JVM arguments required for JavaFX on modern JDKs
    jvmArgs = listOf(
        "--add-opens=java.base/java.lang=ALL-UNNAMED",
        "--add-opens=java.base/java.time=ALL-UNNAMED",
        "--add-opens=com.calendarfx.view/com.calendarfx.view=ALL-UNNAMED",
        "--add-opens=com.calendarfx.view/com.calendarfx.view.page=ALL-UNNAMED",
        "--add-opens=com.calendarfx.view/com.calendarfx.view.popover=ALL-UNNAMED",
        "--add-opens=com.calendarfx.view/com.calendarfx.view.print=ALL-UNNAMED"
    )
}