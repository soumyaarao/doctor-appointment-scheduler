from collections import defaultdict
from dataclasses import dataclass

@dataclass
class TimeSlot:
    dayOfWeek: int # in 0-7
    startTime: int # in minutes starting 0 for 00:00 AM
    endTime: int # in minutes starting 0 for 00:00 AM
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
        self.time_zone_wise_slots = defaultdict(list) # list of TimeSlot
        self.appointments = {} # Pin wise details
        self.are_appointments_full = False

    def add_doctor_slot(self, time_zone, day, start_time, end_time):
        time_slot = TimeSlot(
                        dayOfWeek=day,
                        time_zone=time_zone,
                        startTime=start_time,
                        endTime=end_time,
                    )
        self.time_zone_wise_slots[time_zone].append(time_slot)


    def add_appointment(self, patient_name, time_zone, day, start_time, end_time, pin):
        # return True if possible and booked else False.
        # If pin already used by same person for another
        # booking ask other pin
        pass
    def remove_appointment(self, patient_name, pin):
        pass # return True if removed else False if pin is incorrect

    def show_available_appointments(self):
        pass # return list of available slots

