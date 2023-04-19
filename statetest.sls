{% set stateOutput = salt['state.apply']('jinjatest') | tojson %}
