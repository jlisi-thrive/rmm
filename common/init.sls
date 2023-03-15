highstate_schedule:
  schedule.present:
    - function: state.highstate
    - seconds: 60
    - maxrunning: 1
    - enabled: True

file_override_example:
  file.managed:
    - name: C:/asfaf.txt
    - source: salt://asfaf.txt
