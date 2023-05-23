import json
import requests
import pingparsing
from operator import itemgetter
from datetime import datetime


def sendMineUpdateEvent(mineName, data):
    __salt__["event.send"](
        "thrive/mine/"+__grains__["id"]+"/"+mineName,
        data,
    )


def health():
    # sendMineUpdateEvent("health", {"lastCheckIn": datetime.utcnow(
    # ).isoformat(), "checkInMaster": __grains__["master"]})
    return {"lastCheckIn": datetime.utcnow().isoformat(), "checkInMaster": __grains__["master"]}


# def sendGrains():
#     __salt__["event.send"](
#         "myco/my_custom_module/finished",
#         {"with_grains": True, "message": "Grains Updated"},
#         with_grains=True
#     )
#     return True


def pings():
    destinations = ["8.8.8.8", "8.8.4.4", "thrive.service-now.com"]
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.count = 3
    results = []

    for destination in destinations:
        transmitter.destination = destination
        result = transmitter.ping()
        response = ping_parser.parse(result)
        resObj = {
            'destination': response.destination,
            'min': response.rtt_min,
            'max': response.rtt_max,
            'avg': response.rtt_avg
        }
        results.append(resObj)
    # sendMineUpdateEvent("pings", {"lastCheckIn": datetime.utcnow(
    #     ), "checkInMaster": __grains__["master"]})
    # __salt__["grains.setval"]("pings", results)
    return results
