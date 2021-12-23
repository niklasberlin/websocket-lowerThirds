import datetime

import models
import requests

SCHEDULE_URL = "https://pretalx.c3voc.de/rc3-2021-xhain/schedule/export/schedule.json"

def get_talks(schedule):
    for day in schedule["conference"]["days"]:
        for room in day["rooms"].values():
            for talk in room:
                yield talk


def update_from_schedule(storage: models.Storage, schedule_url: str = SCHEDULE_URL):
    schedule = requests.get(schedule_url).json()['schedule']

    for talk in get_talks(schedule):
        print(talk)
        for person in talk["persons"]:
            if person["code"] not in storage.lower_thirds:
                storage.lower_thirds[person["code"]] = models.LowerThirdEntry(
                    first_line=person["public_name"],
                    second_line="",
                    delay=5000,
                )
        if talk["guid"] not in storage.talks:
            hours, mins = talk["duration"].split(":")
            duration = datetime.timedelta(hours=int(hours), minutes=int(mins))
            storage.talks[talk["guid"]] = models.TalkEntry(
                name=talk["title"],
                start=datetime.datetime.fromisoformat(talk["date"]),
                duration=duration,
                lower_thirds=[x["code"] for x in talk["persons"]],
            )
        else:
            storage.talks[talk["guid"]].lower_thirds = [
                x["code"] for x in talk["persons"]
            ]

    storage.version = schedule['version']

    return storage
