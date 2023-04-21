from salt.tokens.localfs import list_tokens
import salt.config


def get_tokens():
    master_opts = salt.config.client_config('/etc/salt/master')
    tokens = list_tokens(master_opts)
    return tokens
