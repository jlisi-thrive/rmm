disable_lmhost:
  reg.present:
    - name: HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters
    - vname: EnableLMHOSTS
    - vdata: 0
    - vtype: REG_DWORD
