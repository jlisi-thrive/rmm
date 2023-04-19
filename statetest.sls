{% set stateOutput = salt['state.apply']('set_customgrain') | tojson %}
