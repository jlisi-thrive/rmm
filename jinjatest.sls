{% set theContext = show_full_context()|yaml(False) %}

run_echo:
  cmd.run:
    - name: echo '{{theContext}}'