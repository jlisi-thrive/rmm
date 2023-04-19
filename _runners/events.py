import json
from azure.eventgrid import EventGridPublisherClient,EventGridEvent
from azure.core.credentials import AzureKeyCredential

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
