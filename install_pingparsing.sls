install_pingparsing:
  pip.installed:
    - name: pingparsing
    #- cwd: 'C:\Program Files\Salt Project\Salt\bin\Scripts'
    #- bin_env: 'C:\Program Files\Salt Project\Salt\bin\Scripts\pip.exe'
    - bin_env: 'C:\Program Files\Salt Project\Salt\salt-pip.bat'
    #- pip_bin: 'C:\Program Files\Salt Project\Salt\bin\pip'
    - upgrade: True
