import click

from appointment import DoctorSchedule
from doctor import Doctor, DoctorViewModel

@click.group()
def cli():
    display_available_slots()
    book_appointment()
    cancel_appointment()
    print_full_schedule()

@click.command()
@click.option('--doctor_name', prompt='Enter the doctor\'s name')
def display_available_slots(doctor_name):
    model = DoctorSchedule(doctor_name)
    slots = model.get_available_slots(doctor_name)
    print("\nAvailable slots:")
    for slot in slots:
        print(slot)


@click.command()
@click.option('--doctor_name', prompt='Enter the doctor\'s name')
@click.option('--user_name', prompt='Enter your name')
@click.option('--user_pin', prompt='Enter your PIN')
@click.option('--user_timezone', prompt='Enter your timezone')
def book_appointment(doctor_name, user_name, user_pin, user_timezone):
    model = Doctor()
    view_model = DoctorViewModel(model)
    slots = view_model.get_available_slots(doctor_name, user_timezone)
    click.echo("\nAvailable slots:")
    for slot in slots:
        click.echo(slot)
    appointment_time_str = click.prompt('Enter the preferred time for the appointment', type=str)
    appointment_time = model.convert_to_utc(appointment_time_str, user_timezone)
    result = model.book_appointment(doctor_name, user_name, user_pin, user_timezone, appointment_time)
    click.echo(result)


@click.command()
@click.option('--user_name', prompt='Enter your name')
@click.option('--user_pin', prompt='Enter your PIN')
def cancel_appointment(user_name, user_pin):
    model = Doctor()
    result = model.cancel_appointment(user_name, user_pin)
    click.echo(result)


@click.command()
def print_full_schedule():
    model = Doctor()
    view_model = DoctorViewModel(model)
    schedule = view_model.get_full_schedule()
    click.echo("\nFull Schedule:")
    for appointment in schedule:
        click.echo(appointment)


cli.add_command(display_available_slots)
cli.add_command(book_appointment)
cli.add_command(cancel_appointment)
cli.add_command(print_full_schedule)

if __name__ == "__main__":
    # cli()
    display_available_slots()
