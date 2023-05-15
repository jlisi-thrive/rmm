import datetime
import logging

import salt.exceptions
import salt.utils.beacons
import salt.utils.platform
import socket
import pymongo

log = logging.getLogger(__name__)

__virtualname__ = "health"


def validate(config):
    """
    Validate the config is a dict
    """
    if not isinstance(config, list):
        return False, "Configuration for status beacon must be a list."
    return True, "Valid beacon configuration"


def __virtual__():
    return __virtualname__


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


def beacon(config):
    """
    Return status for requested information
    """
    log.debug(config)
    mdb = _get_conn(ret=None)
    SOCKET_MASTER = socket.gethostname()
    FQDN_MASTER = SOCKET_MASTER + "-rmm.thrive.management"

    ctime = datetime.datetime.utcnow().isoformat()

    newvalues = {"$set": {"lastCheckIn": ctime, "checkedInHost": FQDN_MASTER}}
    minion = __grains__["id"]
    mdb.minions.update_one({'minion': minion}, newvalues, upsert=True)
    # whitelist = []
    # config = salt.utils.beacons.remove_hidden_options(config, whitelist)

    # if not config:
    #     config = [
    #         {
    #             "loadavg": ["all"],
    #             "cpustats": ["all"],
    #             "meminfo": ["all"],
    #             "vmstats": ["all"],
    #             "time": ["all"],
    #         }
    #     ]

    # if not isinstance(config, list):
    # To support the old dictionary config format
    #    config = [config]

    ret = {}
    # for entry in config:
    #     for func in entry:
    #         ret[func] = {}
    #         try:
    #             data = __salt__["health.{}".format(func)]()
    #         except salt.exceptions.CommandExecutionError as exc:
    #             log.debug(
    #                 "Status beacon attempted to process function %s "
    #                 "but encountered error: %s",
    #                 func,
    #                 exc,
    #             )
    #             continue
    #         if not isinstance(entry[func], list):
    #             func_items = [entry[func]]
    #         else:
    #             func_items = entry[func]
    #         for item in func_items:
    #             if item == "all":
    #                 ret[func] = data
    #             else:
    #                 try:
    #                     try:
    #                         ret[func][item] = data[item]
    #                     except TypeError:
    #                         ret[func][item] = data[int(item)]
    #                 except KeyError as exc:
    #                     ret[
    #                         func
    #                     ] = "Status beacon is incorrectly configured: {}".format(exc)

    return [{"tag": ctime, "data": ret}]
