schedule:
  apply_highstate:
    - function: state.highstate
    - seconds: 60

file_override_example:
  file.managed:
    - name: C:/asfaf.txt
    - source: salt://asfaf.txt
