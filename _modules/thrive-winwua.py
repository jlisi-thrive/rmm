import salt.client
import salt.runner
import salt.config
import salt.utils


def is_connected():
    opts = salt.config.master_config('/etc/salt/master')
    runner = salt.runner.RunnerClient(opts)
    ckminions = salt.utils.minions.CkMinions(opts)
    return ckminions.connected_ids()
