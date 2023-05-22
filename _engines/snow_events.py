"""
A simple test engine, not intended for real use but as an example
"""

import logging
import salt.utils.event
import salt.utils.http
import salt.utils.json


def __virtual__():
    return True


log = logging.getLogger("snow_events")

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

__virtualname__ = "snow_events"


def event_bus_context(opts):
    if opts["__role"] == "master":
        event_bus = salt.utils.event.get_master_event(
            opts, opts["sock_dir"], listen=True
        )
        log.critical("test engine for master started")
    else:
        event_bus = salt.utils.event.get_event(
            "minion",
            opts=opts,
            sock_dir=opts["sock_dir"],
            listen=True,
        )
        log.critical("test engine for minion started")
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
                event = event_bus.get_event()
                log.critical("SENDING EVENT")
                if event:
                    payload = salt.utils.json.dumps(event)
                    salt.utils.http.query(
                        "https://thrivedev.service-now.com/api/global/em/jsonv2",
                        "POST",
                        header_dict={"Content-Type": "application/json",
                                     "Authorization": SNOW_ACCT_AUTH},
                        data=salt.utils.json.dumps({"records":
                                                    [
                                                        {
                                                            "source": "ThriveRMM",
                                                            "event_class": "SCOM 2007 on scom.server.com",
                                                            "resource": "C:",
                                                            "node": "name.of.node.com",
                                                            "metric_name": "Percentage Logical Disk Free Space",
                                                            "type": "RMM Event",
                                                            "severity": "4",
                                                            "description": "The disk C: on computer V-W2K8-dfg.dfg.com is running out of disk space. The value that exceeded the threshold is 41% free space.",
                                                            "additional_info": payload
                                                        }
                                                    ]
                                                    })
                    )
