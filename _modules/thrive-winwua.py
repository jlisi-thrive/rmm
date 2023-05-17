import salt.client
import salt.runner
import salt.config
import salt.utils


def is_connected():
    opts = salt.config.master_config('/etc/salt/master')
    local = salt.client.LocalClient()
    local.cmd('*', 'test.fib', [10])
