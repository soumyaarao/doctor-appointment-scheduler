import csv
from datetime import datetime, timezone

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
                available_start_time = self.convert_to_user_timezone(slot['Available at'], slot['Timezone'], user_timezone)
                available_end_time = self.convert_to_user_timezone(slot['Available until'], slot['Timezone'], user_timezone)
                if self.is_valid_time(appointment_time, available_start_time, available_end_time) and \
                        not self.is_slot_booked(doctor_name, appointment_time):
                    self.appointments[doctor_name].append({'Name': user_name, 'PIN': user_pin, 'Time': appointment_time})
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
        time_format = "%I:%M%p"
        from_zone = timezone(timezone.utc)
        to_zone = timezone(to_timezone)
        utc_time = datetime.strptime(time_str, time_format).replace(tzinfo=from_zone)
        user_time = utc_time.astimezone(to_zone).strftime(time_format)
        return user_time

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

    def get_available_slots(self, doctor_name, user_timezone):
        available_slots = []
        for slot in self.model.doctor_schedule:
            if slot['Name'] == doctor_name:
                start_time = self.model.convert_to_user_timezone(slot['Available at'], slot['Timezone'], user_timezone)
                end_time = self.model.convert_to_user_timezone(slot['Available until'], slot['Timezone'], user_timezone)
                available_slots.append(f"{slot['Day of Week']}: {start_time} - {end_time}")
        return available_slots

    def get_full_schedule(self):
        return self.model.print_full_schedule()