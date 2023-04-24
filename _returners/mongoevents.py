import logging
import json
import socket
from enum import Enum
from azure.eventhub import EventHubProducerClient, EventData

import uuid
import salt.returners
import salt.utils.jid


try:
    import pymongo

    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = "mongoevents"


def __virtual__():
    if not HAS_PYMONGO:
        return False, "Could not import mongo returner; pymongo is not installed."
    return __virtualname__


def _remove_dots(src):
    """
    Remove the dots from the given data structure
    """
    output = {}
    for key, val in src.items():
        if isinstance(val, dict):
            val = _remove_dots(val)
        output[key.replace(".", "-")] = val
    return output


def _get_options(ret=None):
    """
    Get the mongo options from salt.
    """
    attrs = {
        "host": "host",
        "port": "port",
        "db": "db",
        "user": "user",
        "password": "password",
        "indexes": "indexes",
        "uri": "uri",
    }

    _options = salt.returners.get_returner_options(
        __virtualname__, ret, attrs, __salt__=__salt__, __opts__=__opts__
    )
    return _options


def _get_conn(ret):
    """
    Return a mongodb connection object
    """
    # _options = _get_options(ret)

    uri = __opts__.get("mongo.uri", "Not Set")

    # at some point we should remove support for
    # pymongo versions < 2.3 until then there are
    # a bunch of these sections that need to be supported
    pymongo.uri_parser.parse_uri(uri)
    conn = pymongo.MongoClient(uri)
    mdb = conn.get_database()

    return conn, mdb


def returner(ret):
    """
    Return data to a mongodb server
    """
    conn, mdb = _get_conn(ret)

    if isinstance(ret["return"], dict):
        back = _remove_dots(ret["return"])
    else:
        back = ret["return"]

    if isinstance(ret, dict):
        full_ret = _remove_dots(ret)
    else:
        full_ret = ret

    log.debug(back)
    sdata = {
        "minion": ret["id"],
        "jid": ret["jid"],
        "return": back,
        "fun": ret["fun"],
        "full_ret": full_ret,
    }
    if "out" in ret:
        sdata["out"] = ret["out"]

    # save returns in the saltReturns collection in the json format:
    # { 'minion': <minion_name>, 'jid': <job_id>, 'return': <return info with dots removed>,
    #   'fun': <function>, 'full_ret': <unformatted return with dots removed>}
    #
    # again we run into the issue with deprecated code from previous versions

    mdb.saltReturns.insert_one(sdata.copy())


def _safe_copy(dat):
    """ mongodb doesn't allow '.' in keys, but does allow unicode equivs.
        Apparently the docs suggest using escaped unicode full-width
        encodings.  *sigh*

            \\  -->  \\\\
            $  -->  \\\\u0024
            .  -->  \\\\u002e

        Personally, I prefer URL encodings,

        \\  -->  %5c
        $  -->  %24
        .  -->  %2e


        Which means also escaping '%':

        % -> %25
    """

    if isinstance(dat, dict):
        ret = {}
        for k in dat:
            r = (
                k.replace("%", "%25")
                .replace("\\", "%5c")
                .replace("$", "%24")
                .replace(".", "%2e")
            )
            if r != k:
                log.debug("converting dict key from %s to %s for mongodb", k, r)
            ret[r] = _safe_copy(dat[k])
        return ret

    if isinstance(dat, (list, tuple)):
        return [_safe_copy(i) for i in dat]

    return dat


def save_load(jid, load, minions=None):
    """
    Save the load for a given job id
    """
    conn, mdb = _get_conn(ret=None)
    to_save = _safe_copy(load)

    mdb.jobs.insert_one(to_save)


def save_minions(jid, minions, syndic_id=None):  # pylint: disable=unused-argument
    """
    Included for API consistency
    """


def get_load(jid):
    """
    Return the load associated with a given job id
    """
    conn, mdb = _get_conn(ret=None)
    return mdb.jobs.find_one({"jid": jid}, {"_id": 0})


def get_jid(jid):
    """
    Return the return information associated with a jid
    """
    conn, mdb = _get_conn(ret=None)
    ret = {}
    rdata = mdb.saltReturns.find({"jid": jid}, {"_id": 0})
    if rdata:
        for data in rdata:
            minion = data["minion"]
            # return data in the format {<minion>: { <unformatted full return data>}}
            ret[minion] = data["full_ret"]
    return ret


def get_fun(fun):
    """
    Return the most recent jobs that have executed the named function
    """
    conn, mdb = _get_conn(ret=None)
    ret = {}
    rdata = mdb.saltReturns.find_one({"fun": fun}, {"_id": 0})
    if rdata:
        ret = rdata
    return ret


def get_minions():
    """
    Return a list of minions
    """
    conn, mdb = _get_conn(ret=None)
    ret = []
    name = mdb.saltReturns.distinct("minion")
    ret.append(name)
    return ret


def get_jids():
    """
    Return a list of job ids
    """
    conn, mdb = _get_conn(ret=None)
    map = "function() { emit(this.jid, this); }"
    reduce = "function (key, values) { return values[0]; }"
    result = mdb.jobs.inline_map_reduce(map, reduce)
    ret = {}
    for r in result:
        jid = r["_id"]
        ret[jid] = salt.utils.jid.format_jid_instance(jid, r["value"])
    return ret


def prep_jid(nocache=False, passed_jid=None):  # pylint: disable=unused-argument
    """
    Do any work necessary to prepare a JID, including sending a custom id
    """
    return passed_jid if passed_jid is not None else salt.utils.jid.gen_jid(__opts__)


def return_hub(tag):
    if tag == "salt/presence/present":
        return "minion-presence"
    elif tag == "salt/presence/change":
        return "minion-presence"
    else:
        return "rmm-events"


# TODO:: Send to appropriate event hubs based on tag of event
def send_event_data_batch(producer, events):
    event_data_batch = producer.create_batch()
    for event in events:
        event_data_batch.add(EventData(body=json.dumps(event)))
    producer.send_batch(event_data_batch)

# TODO:: Send to appropriate event hubs based on tag of event
# TODO:: Maybe create the event hub if non existing. Read from config?


def send_single_event(producer, event):
    producer.send_event(EventData(body=json.dumps(event)))


def send_event(event):
    EVENT_HUB_CONNECTION_STR = __opts__.get("hub.string", "Not Set")
    FQDN_MASTER = __opts__.get("fqdn", "Not Set")
    tag, data = event["tag"], event["data"]
    jid = data["jid"] if data.__contains__('a') else uuid.uuid4()
    log.critical("From Event Manager")
    # log.critical(data)
    HUB_NAME = return_hub(tag)

    log.critical("Master is: ")
    log.critical(FQDN_MASTER)
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=HUB_NAME)

    event_data = EventData({"tag": tag, "data": data, "master": FQDN_MASTER})
    event_data.content_type = "application/json"

    with producer:
        producer.send_event(event_data)


def send_batch(events):
    for event in events:
        send_event(event)


def event_return(events):
    """
    Return events to Mongodb server
    """
    if isinstance(events, list):
        events = events[0]
        send_event(events)

    if isinstance(events, dict):
        send_batch(events)
    # if isinstance(events, list):
    #     events = events[0]
    #     producer = EventHubProducerClient.from_connection_string(
    #         conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    #     with producer:
    #         send_single_event(producer, events)

    # if isinstance(events, dict):
    #     with producer:
    #         send_event_data_batch(producer, events)
