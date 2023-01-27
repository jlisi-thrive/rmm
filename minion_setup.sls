{% set defaultGateway = salt['ip.get_default_gateway']() %}
{% set minionGrains = salt['grains.items']() | tojson %}
{% set minionId = salt['grains.get']('id') %}
{% set masterId = salt['grains.get']('master') %}

default_gateway:
  grains.present:
    - value: {{defaultGateway}}

sync_modules:
  saltutil.sync_modules:
    - refresh: True
        
snow_event:
  http.query:
    - name: https://thrivedev.service-now.com/api/thn/salt/minion-start/{{masterId}}/{{minionId}}
    - method: POST
    - status: 200
    - header_dict:
        Accept: application/json
        Content-Type: application/json
    - data: '{{minionGrains}}'
