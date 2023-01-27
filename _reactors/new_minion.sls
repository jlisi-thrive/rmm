setup_minion:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - minion_setup
