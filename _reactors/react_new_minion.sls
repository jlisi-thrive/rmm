install_winlogbeat:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - install_winlogbeat

start_winlogbeat:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - start_winlogbeat

install_pingparsing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - test_pip

setup_schedules:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - create_schedule
{# refresh_winrepo:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - test_refresh #}

{# do_first_thing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - set_customgrain #}

{# do_second_thing:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - send_customhttp #}