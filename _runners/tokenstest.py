from salt.tokens.localfs import list_tokens


def get_tokens():
    tokens = list_tokens()
    return tokens
