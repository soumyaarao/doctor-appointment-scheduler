from scheduler import Scheduler
from utils import parse_day, parse_time_in_minutes


def show_available_doctor_schedule(doctor):
    print("\n-----------------------------------------------")
    print("\tBELOW ARE AVAILABLE APPOINTMENTS FOR THE DOCTOR")
    print("-------------------------------------------------")
    for av_appointment in doctor.show_available_appointments():
        print(av_appointment)
    print()


def ask_for_doctor_name(sch):
    print("\n----------------------------------------------------")
    print("\tADD OR REMOVE DOCTOR APPOINTMENTS")
    print("------------------------------------------------------")
    print("\nSelect number for the corresponding doctor name")
    doctor_names = sch.show_doctors_with_available_slots()
    for i in range(len(doctor_names)):
        print(f"{i + 1} : {doctor_names[i].doctor_name}")
    num = int(input("\nSelect doctor : "))
    doctor = doctor_names[num - 1]
    show_available_doctor_schedule(doctor)

    print("B : Book Appointment")
    print("R : Remove Appointment")
    print("H : Home")

    return doctor


def ask_for_booking_details(doctor):
    name = input("\nEnter patient name : ")

    print("\nBelow are the doctor's timezone indexes -")
    time_zones = list(set(doctor.time_zone_wise_slots.keys()))
    for i in range(len(time_zones)):
        print(f"{i + 1} : {time_zones[i]}")
    num = int(input("\nEnter timezone index : "))
    time_zone = time_zones[num - 1]
    day = input("Enter day : ")
    start_time = input("Enter start time(in AM/PM) : ")
    end_time = input("Enter end time : ")
    pin = input("Enter booking pin : ")

    success, error = doctor.add_appointment(
        name,
        time_zone,
        parse_day(day),
        parse_time_in_minutes(start_time),
        parse_time_in_minutes(end_time),
        pin
    )

    if success:
        print("\nBooking done successfully!")
    else:
        print("\nBooking failed.", error)
        print("Please retry!!!")
    print("\nH : Home")


def ask_for_cancellation_details(doctor):
    name = input("\nEnter patient name :")
    pin = input("Enter booking pin :")

    success, error = doctor.remove_appointment(name, pin)
    if success:
        print("\nBooking cancelled!")
    else:
        print("\nCancellation failed.", error)
        print("Please retry!!!")
    print("\nH : Home")


if __name__ == "__main__":
    sch = Scheduler()
    ch = "H"
    doctor = None

    while ch != "E":
        try:
            if ch == "H":
                doctor = ask_for_doctor_name(sch)
            elif ch == "B":
                ask_for_booking_details(doctor)
            elif ch == "R":
                ask_for_cancellation_details(doctor)
            else:
                print("Choose amongst available options only!")
        except Exception as e:
            print("Please enter valid input and retry")
            print(f"Error :", e, "\n")
        print("E : Exit")
        ch = input("\n\nEnter Option : ")
