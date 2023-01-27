sync_modules:
  saltutil.sync_modules:
    - refresh: True
    
disk_grain:
    schedule.present:
        - function: thrive-custom.setDiskUsageGrain
        - seconds: 60
        - maxrunning: 1
        - enabled: True

{# ping_grain:
    schedule.present:
        - function: thrive-custom.setPingGrain
        - seconds: 60
        - maxrunning: 1
        - enabled: True #}

{# events_schedule:
    schedule.present:
        - function: thrive-custom.windowsEventLogWatcher
        - seconds: 60
        - maxrunning: 1
        - enabled: True #}
