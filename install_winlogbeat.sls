winlogbeat:
  pkg.installed:
    - refresh: False

push_winlogbeatconfig:
  file.managed:
    - name: C:\Program Files\Winlogbeat\winlogbeat.yml
    - source: salt://winlogbeat.yml
    - force: True