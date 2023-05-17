import salt.client
import salt.runner
import salt.config


def is_connected():
    opts = salt.config.master_config('/etc/salt/master')
    runner = salt.runner.RunnerClient(opts)
    return runner.cmd('manage.up', [])
