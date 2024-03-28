import re

DAYS_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def days_between(start_day: str, end_day: str) -> list:
    start_day = start_day.upper()
    end_day = end_day.upper()

    start_index = DAYS_OF_WEEK.index(start_day)
    end_index = DAYS_OF_WEEK.index(end_day)

    if start_index <= end_index:
        return DAYS_OF_WEEK[start_index : end_index + 1]
    else:
        return DAYS_OF_WEEK[start_index:] + DAYS_OF_WEEK[: end_index + 1]


def extract_close_from_text(text: str) -> str:
    pattern = r"(?i)(?=.*close)(?=.*(mon|tue|wed|thu|fri|sat|sun)).*"
    matches = re.findall(pattern, text)
    for match in matches:
        return match.upper()
    return ""


def extract_fasting_hours_from_text(text: str) -> dict:
    if "fastingmonth:" not in text.lower():
        return {}
    pattern = r"(?i)(fastingmonth:)\n(mon|tue|wed|thu|fri|sat|sun)?.*(mon|tue|wed|thu|fri|sat|sun)[^0-9]*(\d{1,2}:\d{2}[AP]M)[^0-9]*(\d{1,2}:\d{2}[AP]M)"
    hours_dict = {}
    matches = re.findall(pattern, text)

    for match in matches:
        end_day = match[2].upper()
        start_day = match[1].upper() if match[2] else end_day
        start_time = match[3]
        end_time = match[4]

        for day in days_between(start_day, end_day):
            hours_dict[day] = f"{start_time} - {end_time}"

    return hours_dict


def extract_hours_from_text(text: str) -> dict:
    hours_dict = {}

    pattern = r"(?i)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)?.*(monday|tuesday|wednesday|thursday|friday|saturday|sunday)[^0-9]*(\d{1,2}:\d{2}[AP]M)[^0-9]*(\d{1,2}:\d{2}[AP]M)"
    matches = re.findall(pattern, text)

    for match in matches:
        end_day = match[1].upper()[:3]
        start_day = match[0].upper()[:3] if match[0] else end_day
        start_time = match[2]
        end_time = match[3]

        # Update the dictionary with the operating hours
        for day in days_between(start_day, end_day):
            hours_dict[day] = f"{start_time} - {end_time}"

    if hours_dict:
        return hours_dict

    pattern = r"(?i)(mon|tue|wed|thu|fri|sat|sun)?.*(mon|tue|wed|thu|fri|sat|sun)[^0-9]*(\d{1,2}[AP]M)[^0-9]*(\d{1,2}[AP]M)"
    matches = re.findall(pattern, text)

    for match in matches:
        end_day = match[1].upper()
        start_day = match[0].upper() if match[0] else end_day
        start_time = match[2]
        end_time = match[3]

        # Update the dictionary with the operating hours
        for day in days_between(start_day, end_day):
            hours_dict[day] = f"{start_time} - {end_time}"

    if hours_dict:
        return hours_dict

    pattern = r"(?i)(\d{4})[^0-9]*(\d{4})[^0-9]*(mon|tue|wed|thu|fri|sat|sun).*(mon|tue|wed|thu|fri|sat|sun)"
    matches = re.findall(pattern, text)

    for match in matches:
        start_time = match[0]
        end_time = match[1]
        start_day = match[2].upper()
        end_day = match[3].upper()

        # Update the dictionary with the operating hours
        for day in days_between(start_day, end_day):
            hours_dict[day] = f"{start_time} - {end_time}"

    return hours_dict
