{% set stateOutput = salt['state.apply']('set_customgrain') | tojson %}

thrive/mystaterun:
  event.send:
    - data: {{stateOutput}}
