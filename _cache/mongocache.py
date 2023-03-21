import errno
import logging
import os
import os.path
import shutil
import json
import requests
import base64
import tempfile
import socket
import copy
import time

import salt.payload
import salt.utils.stringutils
import salt.utils.jid
from salt.utils.versions import Version
import salt.utils.atomicfile
import salt.utils.files
from salt.exceptions import SaltCacheError

try:
    import pymongo

    PYMONGO_VERSION = Version(pymongo.version)
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = "mongocache"

__func_alias__ = {"list_": "list"}

def __virtual__():
    return __virtualname__

def _get_conn(ret):
    """
    Return a mongodb connection object
    """
    _options = _get_options(ret)

    host = _options.get("host")
    port = _options.get("port")
    uri = _options.get("uri")
    db_ = _options.get("db")
    user = _options.get("user")
    password = _options.get("password")
    indexes = _options.get("indexes", False)

    # at some point we should remove support for
    # pymongo versions < 2.3 until then there are
    # a bunch of these sections that need to be supported
    if uri and PYMONGO_VERSION > Version("2.3"):
        if uri and host:
            raise salt.exceptions.SaltConfigurationError(
                "Mongo returner expects either uri or host configuration. Both were"
                " provided"
            )
        pymongo.uri_parser.parse_uri(uri)
        conn = pymongo.MongoClient(uri)
        mdb = conn.get_database()
    else:
        if PYMONGO_VERSION > Version("2.3"):
            conn = pymongo.MongoClient(host, port, username=user, password=password)
        else:
            if uri:
                raise salt.exceptions.SaltConfigurationError(
                    "pymongo <= 2.3 does not support uri format"
                )
            conn = pymongo.Connection(host, port, username=user, password=password)

        mdb = conn[db_]

    if indexes:
        if PYMONGO_VERSION > Version("2.3"):
            mdb.minionCache.create_index("minion")
            #mdb.minionCache.create_index("jid")
        else:
            mdb.minionCache.ensure_index("minion")
            #mdb.minionCache.ensure_index("jid")

    return conn, mdb

def get_snow_auth_header():
    snuri = __opts__.get("snuri", "Not Set")
    snuser = __opts__.get("snuser", "Not Set")
    snpass =__opts__.get("snpass", "Not Set")
    userpass = snuser+":"+snpass
    encoded_u = base64.b64encode(userpass.encode()).decode()
    headers = {"Authorization" : "Basic %s" % encoded_u, "Accept": "application/json"}
    return headers

def __cachedir(kwargs=None):
    if kwargs and "cachedir" in kwargs:
        return kwargs["cachedir"]
    return __opts__.get("cachedir", salt.syspaths.CACHE_DIR)


def init_kwargs(kwargs):
    return {"cachedir": __cachedir(kwargs)}


def get_storage_id(kwargs):
    return ("localfs", __cachedir(kwargs))


def store(bank, key, data, cachedir):
    """
    Store information in a file.
    """
    print("Storing information in cache for bank " + bank + " and key " + key + "")
    bankSplit = bank.split("/")
    minion = bankSplit[1]
    #snuri = __opts__.get("snuri", "Not Set")
    conn, mdb = _get_conn(ret=None)
    #headers = get_snow_auth_header()
    #url = snuri + "/api/thn/salt/cache/" + minion
    payload = json.dumps({"host": socket.gethostname(), "minion": minion, "bank": bank, "key": key, "data": data, "action": "store"})
    mdb.minionCache.insert_one(payload.copy())
    #requests.request("POST", url, data=payload, headers=headers)
    base = os.path.join(cachedir, os.path.normpath(bank))
    try:
        os.makedirs(base)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise SaltCacheError(
                "The cache directory, {}, could not be created: {}".format(base, exc)
            )

    outfile = os.path.join(base, "{}.p".format(key))
    tmpfh, tmpfname = tempfile.mkstemp(dir=base)
    os.close(tmpfh)
    try:
        with salt.utils.files.fopen(tmpfname, "w+b") as fh_:
            salt.payload.dump(data, fh_)
        # On Windows, os.rename will fail if the destination file exists.
        salt.utils.atomicfile.atomic_rename(tmpfname, outfile)
    except OSError as exc:
        raise SaltCacheError(
            "There was an error writing the cache file, {}: {}".format(base, exc)
        )


def fetch(bank, key, cachedir):
    """
    Fetch information from a file.
    """
    print("Fetching information in cache for bank " + bank + " and key " + key + "")
    inkey = False
    bankSplit = bank.split("/")
    minion = bankSplit[1]
    url = "https://thrivedev.service-now.com/api/thn/salt/cache/" + minion
    saltReturn = ""
    key_file = os.path.join(cachedir, os.path.normpath(bank), "{}.p".format(key))
    if not os.path.isfile(key_file):
        # The bank includes the full filename, and the key is inside the file
        key_file = os.path.join(cachedir, os.path.normpath(bank) + ".p")
        inkey = True

    if not os.path.isfile(key_file):
        log.debug('Cache file "%s" does not exist', key_file)
        return {}
    try:
        with salt.utils.files.fopen(key_file, "rb") as fh_:
            if inkey:
                saltReturn = salt.payload.load(fh_)[key]
            else:
                saltReturn = salt.payload.load(fh_)
        #payload = json.dumps({"bank": bank, "key": key, "data": saltReturn, "action": "fetch"})
        #requests.request("POST", url, data=payload, headers={'Content-Type': 'application/json'})
        return saltReturn
    except OSError as exc:
        raise SaltCacheError(
            'There was an error reading the cache file "{}": {}'.format(key_file, exc)
        )


def updated(bank, key, cachedir):
    """
    Return the epoch of the mtime for this cache file
    """
    print("Updated information in cache for bank " + bank + " and key " + key + "")
    key_file = os.path.join(cachedir, os.path.normpath(bank), "{}.p".format(key))
    if not os.path.isfile(key_file):
        log.warning('Cache file "%s" does not exist', key_file)
        return None
    try:
        return int(os.path.getmtime(key_file))
    except OSError as exc:
        raise SaltCacheError(
            'There was an error reading the mtime for "{}": {}'.format(key_file, exc)
        )


def flush(bank, key=None, cachedir=None):
    """
    Remove the key from the cache bank with all the key content.
    """
    if cachedir is None:
        cachedir = __cachedir()

    try:
        if key is None:
            target = os.path.join(cachedir, os.path.normpath(bank))
            if not os.path.isdir(target):
                return False
            shutil.rmtree(target)
        else:
            target = os.path.join(cachedir, os.path.normpath(bank), "{}.p".format(key))
            if not os.path.isfile(target):
                return False
            os.remove(target)
    except OSError as exc:
        raise SaltCacheError('There was an error removing "{}": {}'.format(target, exc))
    return True


def list_(bank, cachedir):
    """
    Return an iterable object containing all entries stored in the specified bank.
    """
    print("Listing information in cache for bank " + bank)
    base = os.path.join(cachedir, os.path.normpath(bank))
    if not os.path.isdir(base):
        return []
    try:
        items = os.listdir(base)
    except OSError as exc:
        raise SaltCacheError(
            'There was an error accessing directory "{}": {}'.format(base, exc)
        )
    ret = []
    for item in items:
        if item.endswith(".p"):
            ret.append(item.rstrip(item[-2:]))
        else:
            ret.append(item)
    return ret


def contains(bank, key, cachedir):
    """
    Checks if the specified bank contains the specified key.
    """
    print("Checking if bank contains information in cache for bank " + bank + " and key " + key + "")
    if key is None:
        base = os.path.join(cachedir, os.path.normpath(bank))
        return os.path.isdir(base)
    else:
        keyfile = os.path.join(cachedir, os.path.normpath(bank), "{}.p".format(key))
        return os.path.isfile(keyfile)
