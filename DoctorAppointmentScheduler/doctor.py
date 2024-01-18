import csv
from appointment import DoctorSchedule


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
    weekday = name_to_num.get(day.lower(), None)
    if weekday is None:
        raise Exception(f"{day} is not a valid weekday/weekend name")
    return weekday


def parse_time_in_minutes(time_in_str):
    is_pm = "pm" in time_in_str.lower()
    if ":" not in time_in_str:
        parsed_minutes = 0
        hours = int(time_in_str.lower().replace("pm", "").replace("am", ""))
    else:
        hours = int(time_in_str.split(":")[0])
        parsed_minutes = int(time_in_str.split(":")[1][:2])
    if is_pm:
        hours += 12
    minutes = hours * 60 + parsed_minutes
    return minutes


def parse_time_from_minutes(time_in_int):
    hrs = time_in_int // 60
    minutes = time_in_int - (hrs * 60)
    is_pm = True if hrs >= 12 else False
    if is_pm:
        hrs -= 12
    return f"{hrs}:{minutes}{'PM' if is_pm else 'AM'}"


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
