from datetime import datetime
import re
from typing import Dict, List, Tuple

DAYS_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


class OperatingHoursExtractor:
    def __init__(self):
        self.patterns = [
            {
                "regex": r"(?i)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)?.*(monday|tuesday|wednesday|thursday|friday|saturday|sunday)[^0-9]*(\d{1,2}:\d{2}[AP]M)[^0-9]*(\d{1,2}:\d{2}[AP]M)",
                "extractor": self._extract_pattern_1,
            },
            {
                "regex": r"(?i)(mon|tue|wed|thu|fri|sat|sun)?.*(mon|tue|wed|thu|fri|sat|sun)[^0-9]*(\d{1,2}[AP]M)[^0-9]*(\d{1,2}[AP]M)",
                "extractor": self._extract_pattern_2,
            },
            {
                "regex": r"(?i)(\d{4})[^0-9]*(\d{4})[^0-9]*(mon|tue|wed|thu|fri|sat|sun).*(mon|tue|wed|thu|fri|sat|sun)",
                "extractor": self._extract_pattern_3,
            },
        ]

        self.fasting_patterns = [
            {
                "regex": r"(?i)(fastingmonth:)\n(mon|tue|wed|thu|fri|sat|sun)?.*(mon|tue|wed|thu|fri|sat|sun)[^0-9]*(\d{1,2}:\d{2}[AP]M)[^0-9]*(\d{1,2}:\d{2}[AP]M)",
                "extractor": self._extract_fasting_pattern,
            },
        ]

    def _extract_pattern_1(
        self, match: Tuple[str, ...]
    ) -> Tuple[str, str, datetime, datetime]:
        end_day = match[1].upper()[:3]
        start_day = match[0].upper()[:3] if match[0] else end_day
        start_time = datetime.strptime(match[2].upper(), "%I:%M%p")
        end_time = datetime.strptime(match[3].upper(), "%I:%M%p")
        return start_day, end_day, start_time, end_time

    def _extract_pattern_2(
        self, match: Tuple[str, ...]
    ) -> Tuple[str, str, datetime, datetime]:
        end_day = match[1].upper()
        start_day = match[0].upper() if match[0] else end_day
        start_time = datetime.strptime(match[2].upper(), "%I%p")
        end_time = datetime.strptime(match[3].upper(), "%I%p")
        return start_day, end_day, start_time, end_time

    def _extract_pattern_3(
        self, match: Tuple[str, ...]
    ) -> Tuple[str, str, datetime, datetime]:
        start_time = datetime.strptime(match[0], "%H%M")
        end_time = datetime.strptime(match[1], "%H%M")
        start_day = match[2].upper()
        end_day = match[3].upper()
        return start_day, end_day, start_time, end_time

    def _extract_fasting_pattern(
        self, match: Tuple[str, ...]
    ) -> Tuple[str, str, str, str]:
        end_day = match[2].upper()
        start_day = match[1].upper() if match[2] else end_day
        start_time = match[3]
        end_time = match[4]
        return start_day, end_day, start_time, end_time

    def _extract_hours_from_text(self, text: str, patterns: List[Dict]) -> Dict:
        hours_dict = {}
        for pattern in patterns:
            matches = re.findall(pattern["regex"], text)
            for match in matches:
                start_day, end_day, start_time, end_time = pattern["extractor"](match)
                for day in self.days_between(start_day, end_day):
                    hours_dict[day] = {"start_time": start_time, "end_time": end_time}
        return hours_dict

    def extract_operating_hours_from_text(self, text: str) -> dict:
        return self._extract_hours_from_text(text, self.patterns)

    def extract_fasting_operating_hours_from_text(self, text: str) -> dict:
        if "fastingmonth:" not in text.lower():
            return {}
        return self._extract_hours_from_text(text, self.fasting_patterns)

    def extract_close_day_from_text(self, text: str) -> str:
        pattern = r"(?i)(?=.*close)(?=.*(mon|tue|wed|thu|fri|sat|sun)).*"
        matches = re.findall(pattern, text)
        for match in matches:
            return match.upper()
        return ""

    def days_between(self, start_day: str, end_day: str) -> list:
        start_day = start_day.upper()
        end_day = end_day.upper()

        start_index = DAYS_OF_WEEK.index(start_day)
        end_index = DAYS_OF_WEEK.index(end_day)

        if start_index <= end_index:
            return DAYS_OF_WEEK[start_index : end_index + 1]
        else:
            return DAYS_OF_WEEK[start_index:] + DAYS_OF_WEEK[: end_index + 1]
