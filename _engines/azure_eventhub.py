import logging
import threading
import time
import json
import salt.utils.event
import salt.utils.json
from azure.eventhub import EventHubConsumerClient, EventData

RECEIVE_DURATION = 15


def __virtual__():
    return True


log = logging.getLogger("azure_eventhub")

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

__virtualname__ = "azure_eventhub"


def on_event(partition_context, event: EventData):
    # Put your code here.
    # If the operation is i/o intensive, multi-thread will have better performance.
    eventBody = event.body_as_json()
    log.debug("Received event from partition: {}.".format(
        partition_context.partition_id))
    log.critical(json.dumps(eventBody))


def on_partition_initialize(partition_context):
    # Put your code here.
    log.debug("Partition: {} has been initialized.".format(
        partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    log.debug("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        log.debug("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        log.debug(
            "An exception: {} occurred during the load balance process.".format(error))


def start():
    fire_master = salt.utils.event.get_master_event(
        __opts__, __opts__["sock_dir"], listen=False
    ).fire_event
    log.critical("Started Event Hub")
    EVENT_HUB_CONNECTION_STR = __opts__.get("hub.string", "Not Set")
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        consumer_group='saltstack',
        eventhub_name="rmm-events",
    )
    log.debug('Consumer will keep receiving for {} seconds, start time is {}.'.format(
        RECEIVE_DURATION, time.time()))

    try:
        thread = threading.Thread(
            target=consumer_client.receive,
            kwargs={
                "on_event": on_event,
                "on_partition_initialize": on_partition_initialize,
                "on_partition_close": on_partition_close,
                "on_error": on_error,
                # "-1" is from the beginning of the partition.
                "starting_position": "-1",
            }
        )
        thread.daemon = True
        thread.start()
        time.sleep(RECEIVE_DURATION)
        consumer_client.close()
        thread.join()
    except KeyboardInterrupt:
        log.debug('Stop receiving.')

    log.debug('Consumer has stopped receiving, end time is {}.'.format(time.time()))
