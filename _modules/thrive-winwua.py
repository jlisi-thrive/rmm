import salt.client
import salt.runner
import salt.config


def getConnectedMinion():
    opts = salt.config.master_config('/etc/salt/master')
    runner = salt.runner.RunnerClient(opts)
    return runner.cmd('manage.up', [])
