winlogbeat:
  service.running:
    - enable: True

{# setup_winlogbeatbeacon:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\beacons.conf
    - source: salt://beacons.conf
    - force: True #}