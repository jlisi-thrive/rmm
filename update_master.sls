update_master_conf:
  file.managed:
    - name: C:\ProgramData\Salt Project\Salt\conf\minion.d\master.conf
    - source: salt://config/minion/master.conf
    - force: True

create_thrivermmsvc_task:
  module.run:
    - name: task.create_task
    - m_name: 'thrive_rmm_restart'
    - user_name: System
    - kwargs:
        action_type: Execute
        cmd: 'powershell'
        arguments: 'Restart-Service ThriveRMM'
        trigger_type: Once

run_thrivermmsvc_task:
  module.run:
    - name: task.run
    - m_name: 'thrive_rmm_restart'