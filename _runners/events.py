import json
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.eventgrid import EventGridPublisherClient,EventGridEvent
from azure.core.credentials import AzureKeyCredential

async def send_single_message(sender, data, subject):
    # Create a Service Bus message and send it to the queue
    message = ServiceBusMessage(body=json.dumps(data), subject=subject)
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
              await send_single_message(sender, data, subject)

def runTopic(data, subject):
    asyncio.run(sendTopic(data, subject))
