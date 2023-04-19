{% set eventData =  data['data'] | tojson %}

send_event:
  runner.events.jobs:
    - args:
      - data: {{ eventData }}
