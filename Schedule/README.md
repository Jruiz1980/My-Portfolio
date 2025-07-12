# Overview

This project is a desktop task scheduling application developed to deepen my understanding of modern Java application development. It serves as a practical exercise in applying object-oriented principles, building graphical user interfaces with JavaFX, and managing data persistence.

The software provides a fully interactive calendar where users can manage their daily activities. Key features include the ability to create, edit, and delete both simple, one-time tasks and complex, recurring tasks. The application leverages the powerful CalendarFX library for its user interface and persists all task data locally to a JSON file, ensuring user data is saved between sessions.

My primary purpose for creating this application was to demonstrate a solid understanding of Java syntax and object-oriented design patterns, particularly polymorphism. By creating a class hierarchy for different types of schedulable items (`SimpleTask`, `RecurringTask`), the application showcases how a single interface (`SchedulableItem`) can be used to manage different objects in a uniform way. Additionally, this project was an opportunity to gain hands-on experience with the JavaFX framework and third-party libraries like Gson.

[Software Demo Video]()

# Development Environment

This application was developed using IntelliJ IDEA as the primary IDE and Gradle for managing dependencies and the build process. Version control was handled with Git and hosted on GitHub.

The core programming language is **Java**. The application is built on the **JavaFX** framework for the user interface. Key external libraries include:

* **CalendarFX**: For the rich, interactive calendar components.
* **Google Gson**: For seamless serialization and deserialization of task objects to and from JSON format.
* **SLF4J**: As a logging facade to provide clear and informative logging during development and runtime.

# Useful Websites

* [Oracle Java Documentation](https://docs.oracle.com/en/java/)
* [OpenJFX (JavaFX)](https://fxdocs.github.io/docs/html5/)
* [CalendarFX Developer Center](https://dlsc-software-consulting-gmbh.github.io/CalendarFX/)
* [Google Gson User Guide](https://www.javaguides.net/p/google-gson-tutorial.html)
* [SLF4J (Simple Logging Facade for Java)](https://slf4j.org/manual.html)

# Future Work

* **User Authentication:** Implement a secure login system to allow different users to manage their own private schedules.
* **Notification System:** Integrate with email (JavaMail) and/or messaging services (like WhatsApp via Twilio) to send users notifications for tasks due on the current day.
* **Database Persistence:** Replace the local JSON file storage with a more robust embedded database solution, such as SQLite or H2, to improve data integrity and query performance.
* **Cloud Sync:** Develop a feature to synchronize tasks with a cloud service, enabling users to access and manage their schedule across multiple devices.
