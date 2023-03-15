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
