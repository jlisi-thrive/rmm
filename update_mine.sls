update_mine_functions:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\mine.conf
    - source: salt://config/minion/mine.conf
    - force: True

create_thrivermmsvc_task:
  module.run:
    - name: task.create_task
    - m_name: 'thrive_rmm_restart'
    - user_name: System
    - kwargs:
        force: True
        action_type: Execute
        cmd: 'powershell'
        arguments: 'Restart-Service ThriveRMM'
        trigger_type: Once