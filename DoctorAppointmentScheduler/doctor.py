import csv
from datetime import datetime, timezone, timedelta
import pytz

from DoctorAppointmentScheduler.appointment import DoctorSchedule


class Doctor:
    def __init__(self):
        self.doctor_schedule = self.load_doctor_schedule()
        self.appointments = {}
        self.is_available = True

    def load_doctor_schedule(self):
        with open('availability.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            schedule = [row for row in reader]
        print(schedule)
        return schedule

    def book_appointment(self, doctor_name, user_name, user_pin, user_timezone, appointment_time):
        for slot in self.doctor_schedule:
            if slot['Name'] == doctor_name:
                if doctor_name not in self.appointments:
                    self.appointments[doctor_name] = []
                available_start_time = slot['Available at']
                available_end_time = slot['Available until']
                time_zone = slot['Timezone']
                if self.is_valid_time(appointment_time, available_start_time, available_end_time) and \
                        not self.is_slot_booked(doctor_name, appointment_time):
                    self.appointments[doctor_name].append(
                        {'Name': user_name, 'PIN': user_pin, 'Time': appointment_time})
                    return f"Appointment booked successfully for {user_name} with {doctor_name} at {appointment_time}"
                else:
                    return "Invalid time or slot already booked. Please choose another time."
        return "Doctor not found in the schedule."

    def cancel_appointment(self, user_name, user_pin):
        for doctor_name, appointments in self.appointments.items():
            for appointment in appointments:
                if appointment['Name'] == user_name and appointment['PIN'] == user_pin:
                    self.appointments[doctor_name].remove(appointment)
                    return f"Appointment canceled successfully for {user_name} with {doctor_name} at {appointment['Time']}"
        return "Appointment not found. Please check your name and PIN."

    def convert_to_user_timezone(self, time_str, from_timezone, to_timezone):
        from_zone = pytz.timezone(from_timezone)
        to_zone = pytz.timezone(to_timezone)

        utc_time = pytz.utc.localize(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
        user_time = utc_time.astimezone(to_zone)
        return user_time.strftime("%Y-%m-%d %H:%M:%S")

    def is_valid_time(self, appointment_time, available_start_time, available_end_time):
        return available_start_time <= appointment_time <= available_end_time

    def is_slot_booked(self, doctor_name, appointment_time):
        if doctor_name in self.appointments:
            for slot in self.appointments[doctor_name]:
                if slot['Time'] == appointment_time:
                    return True
        return False

    def print_full_schedule(self):
        schedule = []
        for doctor_name, appointments in self.appointments.items():
            for appointment in appointments:
                schedule.append(f"{doctor_name}: {appointment['Time']} - Booked by {appointment['Name']}")
        return schedule


class DoctorViewModel:
    def __init__(self, model):
        self.model = model

    def get_available_slots(self, doctor_name):
        available_slots = []
        for slot in self.model.doctor_schedule:
            if slot['Name'] == doctor_name:
                start_time = slot['Available at']
                end_time = slot['Available until']
                time_zone = slot['Timezone']
                available_slots.append(f"{slot['Day of Week']}: {start_time} - {end_time} - {time_zone}")
        return available_slots

    def get_full_schedule(self):
        return self.model.print_full_schedule()


def parse_day(day):
    name_to_num = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    return name_to_num[day.lower()]

def parse_time_in_mins(time_in_str):
    is_pm = "pm" in time_in_str.lower()
    hours = int(time_in_str.split(":")[0])
    parsed_minutes = int(time_in_str.split(":")[1][:2])
    if is_pm:
        hours += 12
    minutes = hours*60 + parsed_minutes
    return minutes

class Scheduler:
    def __init__(self):
        self.doctor_schedules = self.load_doctor_schedules()
        self.appointments = {}
        self.is_available = True

    @staticmethod
    def parse_availability_csv(file_name="availability.csv"):
        header_to_index = {}
        schedules = []
        with open(file_name) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if not header_to_index and "Name" in row and "Timezone" in row:
                    header_to_index = {header: idx for idx, header in enumerate(row)}
                elif header_to_index and row:
                    schedules.append(row)
        return header_to_index, schedules

    def load_doctor_schedules(self):
        header_to_index, schedules = self.parse_availability_csv()
        doctor_schedules = {}
        for schedule in schedules:
            doctor_name = schedule[header_to_index["Name"]]
            if doctor_name not in doctor_schedules:
                doctor_schedules[doctor_name] = DoctorSchedule(doctor_name)
            time_zone = schedule[header_to_index["Timezone"]]
            day = parse_day(schedule[header_to_index["Day of Week"]])
            start_time = parse_time_in_mins(schedule[header_to_index["Available at"]])
            end_time = parse_time_in_mins(schedule[header_to_index["Available until"]])
            doctor_schedules[doctor_name].add_doctor_slot(time_zone, day, start_time, end_time)

        return doctor_schedules
