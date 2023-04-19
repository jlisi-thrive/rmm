{% set eventData =  data | tojson %}

send_event:
  runner.events.jobs:
    - args:
      - data: {{ eventData }}
