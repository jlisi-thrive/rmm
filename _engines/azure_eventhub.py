import logging

import salt.utils.event
import salt.utils.json
from azure.eventhub import EventHubProducerClient, EventHubConsumerClient, EventData


def __virtual__():
    return True


log = logging.getLogger(__name__)

__virtualname__ = "azure_eventhub"


def on_event(partition_context, event):
    # Put your code here.
    # If the operation is i/o intensive, multi-thread will have better performance.
    print("Received event from partition: {}.".format(
        partition_context.partition_id))


def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(
        partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def start():
    fire_master = salt.utils.event.get_master_event(
        __opts__, __opts__["sock_dir"], listen=False
    ).fire_event

    EVENT_HUB_CONNECTION_STR = __opts__.get("hub.string", "Not Set")
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        consumer_group='$Default',
        eventhub_name="rmm-events",
    )

    with consumer_client:
        consumer_client.receive(
            on_event=on_event,
            on_partition_initialize=on_partition_initialize,
            on_partition_close=on_partition_close,
            on_error=on_error,
            # "-1" is from the beginning of the partition.
            starting_position="-1",
        )
