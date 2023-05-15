import json
import requests
import pingparsing
import socket
from operator import itemgetter
from datetime import datetime


def health():
    SOCKET_MASTER = socket.gethostname()
    FQDN_MASTER = SOCKET_MASTER + "-rmm.thrive.management"
    return {"lastCheckIn": datetime.now(), "checkInMaster": FQDN_MASTER}


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

    # __salt__["grains.setval"]("pings", results)
    return results
