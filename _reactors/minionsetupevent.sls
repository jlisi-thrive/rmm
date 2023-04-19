{% set eventData =  data | tojson %}

send_event:
  runner.events.minionSetup:
    - args:
      - data: {{ eventData }}
