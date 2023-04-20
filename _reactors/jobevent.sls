{% set eventData =  data | tojson %}

send_event:
  runner.events.runTopic:
    - args:
      - data: {{ eventData }}
      - subject: "job_data"
