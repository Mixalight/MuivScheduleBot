import pandas as pd
from datetime import datetime

import config as cfg
import model as md

def parse_exel() -> md.Schedule:
    df = pd.read_excel(cfg.EXCEL_FILE)
    df = df.dropna(how='all').iloc[8:]

    schedule = md.Schedule(days={})
    current_day_number = None
    lesson_title = None
    start_time = None
    end_time = None
    second_start_time = None
    second_end_time = None
    teacher = None
    room = None
    skip_to_next_day = False
    data = df.values
    save_day = 0

    for r in data:
        row = remove_nan(r)
        if len(row) == 1 and "неделя" in row[0]:
            current_day_number = 0
            continue

        if skip_to_next_day and not isinstance(row[0], datetime):
            continue

        skip_to_next_day = False

        if isinstance(row[0], datetime):
            current_day = cfg.WEEK_DAYS[current_day_number]
            current_day_number += 1
            current_date = row[0]

            if len(row) == 3:
                skip_to_next_day = True
                schedule.days[current_date] = md.Day(weekday=current_day,
                                                  date=current_date,
                                                  lessons=[md.Lesson(
                                                      teacher="",
                                                      title="",
                                                      room="",
                                                      start_time="",
                                                      end_time="")])
                save_day = 0
                continue

            if len(row) == 4:
                if row[3] == "Праздничный день":
                    schedule.days[current_date] = md.Day(weekday=current_day,
                                                      date=current_date,
                                                      lessons=[md.Lesson(
                                                          teacher="",
                                                          title="",
                                                          room="",
                                                          start_time="",
                                                          end_time="")])
                else:
                    lesson_title = row[3]
                    start_time = row[2][:5]
                    end_time = row[2][6:]
                continue


        if len(row) == 1:
            second_start_time = row[0][:5]
            second_end_time = row[0][6:]
            save_day += 1

        if len(row) == 2:
            teacher = row[0]
            room = row[1]
            save_day += 1

        if save_day == 2:
            schedule.days[current_date] = md.Day(weekday=current_day,
                                              date=current_date,
                                              lessons=[
                                                  md.Lesson(
                                                  teacher=teacher,
                                                  title=lesson_title,
                                                  room=room,
                                                  start_time=start_time,
                                                  end_time=end_time),
                                                  md.Lesson(
                                                      teacher=teacher,
                                                      title=lesson_title,
                                                      room=room,
                                                      start_time=second_start_time,
                                                      end_time=second_end_time)
                                              ])
            save_day = 0

    return schedule


def remove_nan(lst: list) -> list:
    return [x for x in lst if not pd.isna(x)]
