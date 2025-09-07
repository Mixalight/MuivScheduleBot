from typing import List

import model as md
import parser as p


def print_lessons(lessons: List):
    for lesson in lessons:
        if lesson.teacher == "":
            print()
        else:
            print(lesson.title, lesson.teacher, lesson.room, f"{lesson.start_time}-{lesson.end_time}", sep=", ")


def print_schedule(schedule: md.Schedule):
    i = 0
    for data, day in schedule.days.items():
        if i == 5:
            i = 0
            print()
        print(day.date.date(), day.weekday, end=": ")
        print_lessons(day.lessons)
        i += 1

def start_bot():
    schedule = p.parse_exel()
    print_schedule(schedule)


def main():
    start_bot()


if __name__ == '__main__':
    main()
