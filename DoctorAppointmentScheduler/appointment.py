from collections import defaultdict
from dataclasses import dataclass

from doctor import Scheduler


@dataclass
class TimeSlot:
    dayOfWeek: int  # in 0-7
    startTime: int  # in minutes starting 0 for 00:00 AM
    endTime: int  # in minutes starting 0 for 00:00 AM
    time_zone: str


@dataclass
class Appointment:
    patient: str
    time_zone: str
    startTime: int
    endTime: int


class DoctorSchedule:
    def __init__(self, doctor_name):
        self.doctor_name = doctor_name
        self.time_zone_wise_slots = defaultdict(list)  # list of TimeSlot
        self.appointments = {}  # Pin wise details
        self.are_appointments_full = False

    def add_doctor_slot(self, time_zone, day, start_time, end_time):
        time_slot = TimeSlot(
            dayOfWeek=day,
            time_zone=time_zone,
            startTime=start_time,
            endTime=end_time,
        )
        self.time_zone_wise_slots[time_zone].append(time_slot)

    def is_valid_time(self, appointment_start_time, appointment_end_time, available_start_time, available_end_time):
        return available_start_time <= appointment_start_time <= appointment_end_time <= available_end_time

    def is_slot_booked(self, doctor_name, appointment_start_time, appointment_end_time):
        if doctor_name == self.doctor_name:
            for appointment in self.appointments:
                existing_start_time = appointment['Available at']
                existing_end_time = appointment['Available until']
                if (
                        (existing_start_time <= appointment_start_time < existing_end_time) or
                        (existing_start_time < appointment_end_time <= existing_end_time) or
                        (appointment_start_time <= existing_start_time and existing_end_time <= appointment_end_time)
                ):
                    return True
        return False

    def get_available_slots(self, doctor_name):
        available_slots = []
        model = Scheduler()
        for slot in model.load_doctor_schedules():
            if slot['Name'] == doctor_name:
                start_time = slot['Available at']
                end_time = slot['Available until']
                time_zone = slot['Timezone']
                available_slots.append(f"{slot['Day of Week']}: {start_time} - {end_time} - {time_zone}")
        return available_slots

    def add_appointment(self, doctor_name, patient_name, time_zone, day, start_time, end_time, pin):
        model = Scheduler()
        for slot in model.load_doctor_schedules():
            if slot['Name'] == doctor_name:
                if pin not in self.appointments:
                    self.appointments[pin] = []
                available_start_time = slot['Available at']
                available_end_time = slot['Available until']
                time_zone = slot['Timezone']
                if self.is_valid_time(start_time, end_time, available_start_time, available_end_time) and \
                        not self.is_slot_booked(doctor_name, start_time, end_time):
                    self.appointments[pin].append(
                        {'Name': patient_name, 'Doctor': doctor_name, 'Time': {start_time} - {end_time}})
                    return f"Appointment booked successfully for {patient_name} with {doctor_name} at {start_time} - {end_time}"
                else:
                    return "Invalid time or slot already booked. Please choose another time."
        return "Doctor not found in the schedule."

    def remove_appointment(self, patient_name, pin):
        for pin, appointments in self.appointments.items():
            for appointment in appointments:
                if appointment['Name'] == patient_name and appointment['PIN'] == pin:
                    self.appointments[doctor_name].remove(appointment)
                    return f"Appointment canceled successfully for {patient_name} with {doctor_name} at {appointment['Time']}"
        return "Appointment not found. Please check your name and PIN."

    def show_available_appointments(self):
        pass  # return list of available slots
