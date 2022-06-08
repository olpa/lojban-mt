from .lexer import lex, TokenClass
from .rafsi import rafsi_to_gismu


def tokenize(text, cb):
    """
    Parse `text` to tokens. For each token, call the callback function
    `cb` with the token as the only parameter.
    """
    rafsi = None
    symbols = None

    def send_rafsi(is_final):
        nonlocal rafsi
        gismu = rafsi_to_gismu(rafsi, default=rafsi)
        if is_final:
            cb(gismu)
        else:
            cb(f'{gismu}##')
        rafsi = None

    def send_symbols(is_final):
        nonlocal symbols
        for sy in symbols[:-1]:
            cb(f'{sy}##')
        if is_final:
            cb(symbols[-1])
        else:
            cb(f'{symbols[-1]}##')
        symbols = None

    def handle_lex_token(token_class, token):
        nonlocal rafsi
        nonlocal symbols
        if symbols:
            is_final = token_class not in {
                    TokenClass.UNKNOWN, TokenClass.QUOTATION}
            send_symbols(is_final)
        if TokenClass.HYPHEN == token_class:
            return
        if rafsi:
            is_final = token_class not in {TokenClass.RAFSI, TokenClass.GISMU}
            send_rafsi(is_final)
        if TokenClass.SKIP == token_class:
            return
        if TokenClass.RAFSI == token_class:
            rafsi = token
            return
        if token_class in {TokenClass.UNKNOWN, TokenClass.QUOTATION}:
            symbols = token
            return
        cb(token)

    lex(text, 0, handle_lex_token)
    if rafsi:
        send_rafsi(is_final=True)
    if symbols:
        send_symbols(is_final=True)


def text_to_tokens(text):
    """
    Parse `text` to a list of tokens.
    """
    tokens = []

    def cb(token):
        tokens.append(token)
    tokenize(text, cb)
    return tokens
