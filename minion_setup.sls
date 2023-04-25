{% set defaultGateway = salt['ip.get_default_gateway']() %}
{% set minionGrains = salt['grains.items']() | tojson %}
{% set minionId = salt['grains.get']('id') %}
{% set masterId = salt['grains.get']('master') %}

default_gateway:
  grains.present:
    - value: {{defaultGateway}}
    - fire_event: thrive/minion_setup/1-4

sync_modules:
  saltutil.sync_modules:
    - refresh: True
    - fire_event: thrive/minion_setup/2-4
    
pingparsing:
  pip.installed:
    - name: pingparsing
    - fire_event: thrive/minion_setup/3-4
    
snow_event:
  http.query:
    - name: https://thrive.service-now.com/api/thn/salt/minion-start/{{masterId}}/{{minionId}}
    - method: POST
    - status: 200
    - header_dict:
        Accept: application/json
        Content-Type: application/json
    - data: '{{minionGrains}}'
    - fire_event: thrive/minion_setup/4-4
