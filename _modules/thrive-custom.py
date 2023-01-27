import json
import requests
import pingparsing
from operator import itemgetter


def testSalt():
    return __grains__["id"]


def windowsEventLogWatcher():
    newestEvent = {}
    with open('C:\Temp\winlogbeat\winlogbeat', encoding="utf8") as f:
        for jsonObj in f:
            eventDict = json.loads(jsonObj)
            newestEvent = eventDict
            break
    eventOutput = json.dumps(newestEvent, separators=(',', ':'))
    minion = __grains__["id"]
    r = requests.post(
        url="https://thrivedev.service-now.com/api/thn/thrivermm/event/"+minion,
        json=newestEvent,
        headers={"Content-Type": "application/json", "Accept": "application/json"})
    return eventOutput


def setDiskUsageGrain():
    usageStats = __salt__["disk.usage"]()
    #__salt__["grains.setval"]("diskUsage", usageStats)
    return usageStats

def setPingGrain():
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

    #__salt__["grains.setval"]("pings", results)
    return results


def setHostUsageMetrics():
    cpustats = __salt__["status.cpustats"]()
    memstats = __salt__["status.meminfo"]()
    __salt__["grains.setval"]("cpuUsage", cpustats)
    __salt__["grains.setval"]("memUsage", memstats)
    return True
