{% set theContext = show_full_context() %}

run_echo:
  cmd.run:
    - name: echo {{theContext}}