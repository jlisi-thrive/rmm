"""
A simple test engine, not intended for real use but as an example
"""

import logging
import salt.utils.event
import salt.utils.http
import salt.utils.json
import fnmatch


def __virtual__():
    return True


log = logging.getLogger("snow_events")

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

__virtualname__ = "snow_events"


def event_bus_context(opts):
    if opts["__role"] == "master":
        event_bus = salt.utils.event.get_event(
            "master",
            opts=opts,
            sock_dir=opts["sock_dir"],
            listen=True,
        )
    else:
        event_bus = salt.utils.event.get_event(
            "minion",
            opts=opts,
            sock_dir=opts["sock_dir"],
            listen=True,
        )
    return event_bus


def start():
    """
    Listen to events and write them to a log file
    """
    log.critical("test engine started")
    with event_bus_context(__opts__) as event_bus:
        SNOW_ACCT_AUTH = __opts__.get("snow.auth", None)
        if (SNOW_ACCT_AUTH):
            while True:
                event = event_bus.get_event(full=True)
                # tag = event["tag"]
                if event is None:
                    continue

                if event:
                    # Check if it is a job
                    target = ""
                    eventData = event["data"]
                    tag = event["tag"] if "tag" in event else None

                    if "thrive/mine" in tag:
                        target = event["tag"].split("/")[2]
                    else:
                        if "id" in eventData:
                            target = eventData["id"]
                        elif "tgt" in eventData:
                            target = eventData["tgt"]
                        else:
                            target = __opts__["id"]
                    payload = salt.utils.json.dumps(
                        eventData, indent=4, sort_keys=True, default=str)
                    salt.utils.http.query(
                        "https://thrivedev.service-now.com/api/global/em/jsonv2",
                        "POST",
                        header_dict={"Content-Type": "application/json",
                                     "Authorization": SNOW_ACCT_AUTH},
                        data=salt.utils.json.dumps({"records":
                                                    [
                                                        {
                                                            "source": "ThriveRMM",
                                                            "event_class": tag,
                                                            "resource": target,
                                                            "node": target,
                                                            "metric_name": tag,
                                                            "type": "RMM Event",
                                                            "severity": "4",
                                                            "description": tag,
                                                            "additional_info": payload
                                                        }
                                                    ]
                                                    })
                    )
