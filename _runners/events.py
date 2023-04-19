import json
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.eventgrid import EventGridPublisherClient,EventGridEvent
from azure.core.credentials import AzureKeyCredential

async def send_single_message(sender, data):
    # Create a Service Bus message and send it to the queue
    message = ServiceBusMessage(body=json.dumps(data), subject="TestSubject")
    await sender.send_messages(message)
    print("Sent a single message")
              
async def sendTopic(data):
  topicConnection = __opts__.get("topic.string", "Not Set")
  topicName = __opts__.get("topic.name", "Not Set")
  async with ServiceBusClient.from_connection_string(
          conn_str=topicConnection,
          logging_enable=True) as servicebus_client:
          sender = servicebus_client.get_topic_sender(topic_name=topicName)
          async with sender:
              await send_single_message(sender, data)

def runTopic(data):
    if data.retcode == 0:
        asyncio.run(sendTopic(data))
            
def jobs(data):
  topicKey = __opts__.get("grid.key", "Not Set")
  topicEndpoint = __opts__.get("grid.endpoint", "Not Set")
  credential = AzureKeyCredential(topicKey)
  client = EventGridPublisherClient(topicEndpoint, credential)
  event = EventGridEvent(
      data=json.dumps(data),
      subject="presence/minionfromrunner",
      event_type="minion_presence",
      data_version="1.0"
  )
  return client.send(event)

def minionSetup(data):
  topicKey = __opts__.get("grid.key", "Not Set")
  topicEndpoint = __opts__.get("grid.endpoint", "Not Set")
  credential = AzureKeyCredential(topicKey)
  client = EventGridPublisherClient(topicEndpoint, credential)
  event = EventGridEvent(
      data=json.dumps(data),
      subject="presence/fromcustomevent",
      event_type="minion_presence",
      data_version="1.0"
  )
  return client.send(event)
