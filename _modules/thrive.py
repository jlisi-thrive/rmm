import json
import requests
from operator import itemgetter
from datetime import datetime

__virtualname__ = "thrive"

try:
    import pingparsing
    HAS_PINGPARSING = True
except ImportError:
    HAS_PINGPARSING = False


def sendMineUpdateEvent(mineName, data):
    __salt__["event.send"](
        "thrive/mine/"+__grains__["id"]+"/"+mineName,
        data,
    )


def mine_data():
    return {
        "u_cpu_usage": __salt__["status.cpuload"](),
        "u_disk_usage": __salt__["disk.usage"](),
        "u_master": __grains__["master"],
        "u_account": __grains__["account_sys_id"],
        "u_cpu": __grains__["cpu_model"],
        "u_domain": __grains__["domain"],
        "u_host": __grains__["host"],
        "u_memory": __grains__["mem_total"],
        "u_number_of_cpus": __grains__["num_cpus"],
        "u_os": __grains__["osfullname"]
    }


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
    if not HAS_PINGPARSING:
        return {}
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
