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
    
pingparsing:
  pip.installed:
    - name: pingparsing