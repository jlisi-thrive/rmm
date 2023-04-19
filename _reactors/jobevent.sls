send_event:
  runner.events.jobs:
    - args:
      - data: {{ data['data']|json }}
