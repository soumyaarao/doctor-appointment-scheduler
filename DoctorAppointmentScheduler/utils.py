name_to_num = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def parse_day(day):
    weekday = name_to_num.get(day.lower(), None)
    if weekday is None:
        raise Exception(f"{day} is not a valid weekday/weekend name")
    return weekday


def get_day_name_from_day(day_num):
    for day_name, day in name_to_num.items():
        if day_num == day:
            return day_name
    raise Exception(f"{day_num} has no corresponding name")


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
