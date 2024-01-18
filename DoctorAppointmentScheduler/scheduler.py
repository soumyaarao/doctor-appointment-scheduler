import csv

from utils import parse_day, parse_time_in_minutes
from appointment import DoctorSchedule


class Scheduler:
    def __init__(self):
        self.doctor_schedules = self.load_doctor_schedules()
        self.appointments = {}

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
            start_time = parse_time_in_minutes(schedule[header_to_index["Available at"]])
            end_time = parse_time_in_minutes(schedule[header_to_index["Available until"]])
            doctor_schedules[doctor_name].add_doctor_slot(time_zone, day, start_time, end_time)

        return doctor_schedules

    def show_doctors_with_available_slots(self):
        doctors = []
        for doctor, doctor_item in self.doctor_schedules.items():
            if doctor_item.are_appointments_full:
                continue
            doctors.append(doctor_item)
        return doctors
