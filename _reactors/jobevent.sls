{% set eventData =  data['data'] %}

send_event:
  runner.events.jobs:
    - args:
      - data: {{ eventData }}
