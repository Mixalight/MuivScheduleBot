from dataclasses import dataclass
from datetime import datetime

from typing import List, Dict

@dataclass
class Lesson:
    teacher: str
    title: str
    room: str
    start_time: str
    end_time: str


@dataclass
class Day:
    weekday: str
    date: datetime
    lessons: List[Lesson]


@dataclass
class Schedule:
    days: Dict[datetime, Day]