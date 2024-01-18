from collections import defaultdict
from dataclasses import dataclass


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
    pin: int


class DoctorSchedule:
    def __init__(self, doctor_name):
        self.doctor_name = doctor_name
        self.time_zone_wise_slots = defaultdict(list)  # list of TimeSlot
        self.appointments = {}
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

    def is_slot_booked(self, appointment_start_time, appointment_end_time):
        for appointment in self.appointments.values():
            existing_start_time = appointment.startTime
            existing_end_time = appointment.endTime
            if (
                    (existing_start_time <= appointment_start_time < existing_end_time) or
                    (existing_start_time < appointment_end_time <= existing_end_time) or
                    (appointment_start_time <= existing_start_time and existing_end_time <= appointment_end_time)
            ):
                return True
        return False

    def get_available_slots(self):
        available_slots = []
        slots = self.time_zone_wise_slots.values()
        slot = None
        for time_slot in slots:
            slot = time_slot
        for sl in slot:
            start_time = sl.startTime
            end_time = sl.endTime
            time_zone = sl.time_zone
            available_slots.append(f"{sl.dayOfWeek}: {start_time} - {end_time} - {time_zone}")
        return available_slots

    def add_appointment(self, patient_name, time_zone, day, start_time, end_time, pin):
        if self.are_appointments_full:
            return False, "Appointments are full for this doctor."

        if not self.time_zone_wise_slots.get(time_zone):
            return False, f"No available slots for the specified timezone ({time_zone})."

        for time_slot in self.time_zone_wise_slots[time_zone]:
            if time_slot.dayOfWeek == day and time_slot.startTime <= start_time < end_time <= time_slot.endTime:
                if not self.is_slot_booked(start_time, end_time):
                    if f"{patient_name}_{pin}" in self.appointments:
                        return False, "Already booked with the same pin for this patient"

                    appointment = Appointment(patient_name, time_zone, start_time, end_time, pin)
                    self.appointments[f"{patient_name}_{pin}"] = appointment
                    all_slots_booked = all(
                        self.is_slot_booked(slot.startTime, slot.endTime)
                        for slots in self.time_zone_wise_slots.values()
                        for slot in slots
                    )
                    if all_slots_booked:
                        self.are_appointments_full = True
                    return True, None
                else:
                    return False, "Slot is already booked for this time period."
        return False, "Time is out of Doctor's Schedule"

    def remove_appointment(self, patient_name, pin):
        if f"{patient_name}_{pin}" not in self.appointments:
            return False, "Appointment not found for this patient."

        appointment = self.appointments[f"{patient_name}_{pin}"]
        if pin != appointment.pin:
            return False, "Invalid PIN for appointment cancellation."

        del self.appointments[f"{patient_name}_{pin}"]
        self.are_appointments_full = False
        return True, None

    def show_available_appointments(self):
        from doctor import parse_time_from_minutes
        available_slots = []

        for time_zone, slots in self.time_zone_wise_slots.items():
            for time_slot in slots:
                start_time = parse_time_from_minutes(time_slot.startTime)
                end_time = parse_time_from_minutes(time_slot.endTime)
                day = time_slot.dayOfWeek

                # Check if the slot is booked
                is_booked = any(
                    appointment.time_zone == time_zone
                    and appointment.startTime == start_time
                    and appointment.endTime == end_time
                    for appointment in self.appointments.values()
                )

                if not is_booked:
                    available_slots.append(f"{day}: {start_time} - {end_time} - {time_zone}")

        return available_slots
