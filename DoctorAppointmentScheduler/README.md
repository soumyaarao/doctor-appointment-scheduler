# Appointment Scheduler README

## Overview
The Appointment Scheduler is a simple command-line application designed to help doctors manage their schedules and patients book or cancel appointments. The system is implemented in Python and utilizes object-oriented programming principles to organize the codebase.

## Project Structure
The project consists of the following files:

1. **appointment.py**: Defines the `TimeSlot` and `Appointment` classes, representing time slots and appointments. It also includes the `DoctorSchedule` class, which manages a doctor's schedule, available slots, and appointments.

2. **main.py**: The main entry point of the application where users can interact with the system. It provides options to select a doctor, book an appointment, cancel an appointment, and exit the application.

3. **scheduler.py**: Manages the overall scheduling system. It loads doctor schedules from a CSV file, maintains a list of doctor schedules, and provides functionality to show available doctors and their appointments.

4. **utils.py**: Contains utility functions used throughout the project, such as parsing days, converting time to minutes, and vice versa.

5. **README.md**: This file. It provides an overview of the project, explains the purpose of each file, and guides users on how to use the system.

## Getting Started
To run the Appointment Scheduler:

1. Unzip the project file.
2. Make sure you have Python installed (version 3.x).
3. Open a terminal in the project directory.

## Running the Application
Run the following command in the terminal to start the application:

```bash
python main.py
```

Follow the on-screen prompts to interact with the system. You can choose a doctor, book appointments, cancel appointments, and exit the application.

## Author
Soumya Rao
