update_mine_functions:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\mine.conf
    - source: salt://config/minion/mine.conf
    - force: True

restart_thrivermm:
  module.run:
    - name: service.restart
    - m_name: ThriveRMM