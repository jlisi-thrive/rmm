{% set eventData =  data | tojson %}

send_event:
  runner.events.sendTopic:
    - args:
      - data: {{ eventData }}
