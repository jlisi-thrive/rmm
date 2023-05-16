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

update_mine_functions:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\mine.conf
    - source: salt://config/minion/mine.conf
    - force: True