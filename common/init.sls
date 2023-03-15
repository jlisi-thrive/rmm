disable_lmhost:
  reg.present:
    - name: HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters
    - vname: EnableLMHOSTS
    - vdata: 0
    - vtype: REG_DWORD
    
disable_smb_v1:
  cmd.run:
    - name: powershell "Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -norestart"
    - stateful: False



# highstate_schedule:
#   schedule.present:
#     - function: state.highstate
#     - seconds: 60
#     - maxrunning: 1
#     - enabled: False

# file_override_example:
#   file.managed:
#     - name: C:/asfaf.txt
#     - source: salt://asfaf.txt
