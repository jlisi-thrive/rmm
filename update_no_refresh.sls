update_no_refresh:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\master.conf
    - source: salt://config/minion/master.conf
    - force: True