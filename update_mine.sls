update_mine_functions:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\mine.conf
    - source: salt://config/minion/mine.conf
    - force: True

create_thrivermmsvc_task:
  module.run:
    - name: task.create
    - m_name: ThriveRMM-restart
    - user_name: System
    - force: True
    - action_type: Execute
    - cmd: 'net stop ThriveRMM && net start ThriveRMM'
    - trigger_type: Once