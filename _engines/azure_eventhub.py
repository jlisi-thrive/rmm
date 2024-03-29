import logging
import json
import salt.client
import salt.utils.event
import salt.utils.json
from azure.eventhub import EventHubConsumerClient, EventData
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore

RECEIVE_DURATION = 15


def __virtual__():
    return True


log = logging.getLogger("azure_eventhub")

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

__virtualname__ = "azure_eventhub"


def on_event(partition_context, event: EventData):
    # Put your code here.
    # If the operation is i/o intensive, multi-thread will have better performance.
    MASTER_FQDN = __opts__.get("master_fqdn", "Not Set")
    try:
        eventBody = event.body_as_json()
        tgt = eventBody["tgt"]
        fun = eventBody["fun"]
        master = eventBody["master"]
        args = eventBody["args"]
        if master == MASTER_FQDN:
            log.critical(tgt)
            log.critical(fun)
            local = salt.client.LocalClient()
            local.cmd_async(tgt, fun, args)
        else:
            log.critical("Not for this master")
    except:
        log.critical("Could not parse")
    partition_context.update_checkpoint(event)


def on_partition_initialize(partition_context):
    # Put your code here.
    log.critical("Partition: {} has been initialized.".format(
        partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    log.critical("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        log.critical("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        log.critical(
            "An exception: {} occurred during the load balance process.".format(error))


def start():
    log.critical("Started Event Hub")
    CHECKPOINT_CONNECTION_STR = __opts__.get("storage.string", "Not Set")
    CHECKPOINT_STORAGE_CONTAINER = __opts__.get("storage.container", "Not Set")
    EVENT_HUB_CONNECTION_STR = __opts__.get("hub.string", "Not Set")
    CONSUMER_GROUP = __opts__.get("consumer_group", "Not Set")
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        CHECKPOINT_CONNECTION_STR, CHECKPOINT_STORAGE_CONTAINER)
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name="rmm-executions",
        checkpoint_store=checkpoint_store
    )
    log.critical('Consumer will keep receiving')

    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                starting_position="-1",
            )
    except KeyboardInterrupt:
        log.critical('Stop receiving.')
