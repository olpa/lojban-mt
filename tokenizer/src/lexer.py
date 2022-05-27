import enum
import re

C_letters = 'bcdfgjklmnprstvxz'
V_letters = 'aeiou'
C = set(C_letters)
V = set(V_letters)
re_skip = re.compile(r'[\s\.]+')
re_hyphen = re.compile(',*[yrnl]?,*')
re_cmavo = re.compile(f"[{C_letters}]?[{V_letters}']+")


@enum.unique
class TokenClass(enum.Enum):
    """
    Token classes returned by the lexer.
    - SKIP: whitespace and dots
    - CMAVO, GISMU, RAFSI: they are
    - HYPHEN: glue content between RAFSI
    - QUOTE_TOKEN, QUOTATION: only for non-lojban quoting ('zoi' and "la'o")
    - MARKUP: non-lojban control sequence
    - UNKNOWN: it is
    """
    UNKNOWN = 0
    SKIP = 1
    CMAVO = 2
    GISMU = 3
    RAFSI = 4
    HYPHEN = 5
    QUOTE_TOKEN = 6
    QUOTATION = 7
    MARKUP = 8


@enum.unique
class T(enum.Enum):
    SKIP = enum.auto()
    AFTER_SKIP = enum.auto()
    TRY_RAFSI = enum.auto()
    AFTER_RAFSI = enum.auto()
    AFTER_HYPHEN = enum.auto()
    TRY_CMAVO = enum.auto()
    QUOTE = enum.auto()
    UNKNOWN = enum.auto()


def re_token(buf, pos, re_, handler):
    m = re_.match(buf[pos:])
    if not m:
        return pos
    next_pos = pos + m.end()
    if handler:
        handler(buf[pos:next_pos])
    return next_pos


# While splitting a word on rafsi components, the lexer tries
# to generate the longest possible rafsi, what is not always right.
#
# Having 'klama' as input, we can parse it as:
# - klama (right)
# - klam a (wrong)
# - kla ma (wrong)
# Having "klama'a", we can parse it as:
# - klama 'a (wrong)
# - kla ma'a (right)
#
# So far, the following heuristics does work: if the next character
# looks like a break, then use the long rafsi
def is_likely_rafsi_break_start(buf, pos):
    if pos >= len(buf):
        return True
    ch = buf[pos]
    # If the next parts start with a vowel,
    # it can't be a rafsi
    if (ch in V) or (ch == "'"):
        return False
    # If it's some break, then it's a rafsi break
    if ch not in C:
        return True
    # Corner case: not in the algorithm but seen in examples ("kulnr,farsi")
    if ('r' == ch) and (pos + 1 < len(buf)) and (buf[pos + 1] == ','):
        return True
    # C
    return False


def lex(buf, pos, handler):
    """
    Lexer for lojban text. Generate input for a tokenizer for machine
    learning, not for syntax parsing. In particular, the lexer doesn't
    care about names and fu'ivla and break them to parts.

    Contract:
    - return correct tokens for valid lojban text that consists
      only of cmavo, lujvo and quotation
    - parse everything
    - If you join the generated tokens, you get the original text

    Input:
    - buf: list of characters
    - pos: starting position in `buf` to parse
    - handler: callback, see output

    Output:
    While parsing, the callback `handler` is called for each token,
    with two parameters: `TokenClass` and the string token
    """
    mode = T.SKIP
    while pos < len(buf):
        ch = buf[pos]

        if T.AFTER_HYPHEN == mode:
            if ch in C:
                mode = T.TRY_RAFSI
            else:
                mode = T.SKIP
            continue

        if T.SKIP == mode:
            pos = re_token(buf, pos, re_skip,
                           lambda s: handler(TokenClass.SKIP, s))
            mode = T.AFTER_SKIP
            continue

        if T.AFTER_SKIP == mode:
            if is_word(buf, pos):
                mode = T.TRY_RAFSI
            else:
                mode = T.TRY_CMAVO
            continue

        # Try rafsi, maybe promote to gismu (CVC/CV or CCVCV)
        if T.TRY_RAFSI == mode:
            if ch not in C:
                mode = T.TRY_CMAVO
                continue
            # Possible input from here:
            # - C(.*)
            if pos + 3 > len(buf):
                mode = T.TRY_CMAVO
                continue
            # Possible input from here:
            # - C..(.*)
            ch2 = buf[pos + 1]
            cvc_p = ch2 in V
            if cvc_p:
                # Possible input from here:
                # - CV.(.*)
                ch3 = buf[pos + 2]
                if ch3 in V:  # CVV
                    handler(TokenClass.RAFSI, buf[pos:pos+3])
                    pos = pos + 3
                    mode = T.AFTER_RAFSI
                    continue
                # Possible input from here:
                # - CV[^V](.*)
                if ((ch3 == "'") and (pos + 3 < len(buf))
                        and (buf[pos + 3])):  # CV'V
                    handler(TokenClass.RAFSI, buf[pos:pos+4])
                    pos = pos + 4
                    mode = T.AFTER_RAFSI
                    continue
                # Possible input from here:
                # - CV[^V'](.*)
                if ch3 not in C:
                    mode = T.TRY_CMAVO
                    continue
            # Possible input from here:
            # - CVC(.*) if `cvc_p` is `True`
            # - C[^V].(.*) otherwise
            if not cvc_p:  # C[^V].(.*)
                if ch2 not in C:
                    mode = T.UNKNOWN
                    continue
                # Possible input from here:
                # - CC.(.*)
                ch3 = buf[pos + 2]
                if ch3 not in V:
                    mode = T.UNKNOWN
                    continue
            # Possible input from here:
            # - CCV(.*)
            # - CVC(.*)
            if pos + 3 == len(buf):
                handler(TokenClass.RAFSI, buf[pos:])
                break
            # Possible input from here:
            # - CCV.(.*)
            # - CVC.(.*)
            ch4 = buf[pos + 3]
            if ch4 not in C:
                # Check for cultural rafsi CCV'VC
                if (("'" == ch4) and (pos + 5) < len(buf)
                        and (buf[pos + 4] in V) and (buf[pos + 5] in C)
                        and is_likely_rafsi_break_start(buf, pos + 6)):
                    rafsi_len = 6
                else:
                    rafsi_len = 3
                # - CCV[^C] can't start gismu or 4-letter rafsi
                handler(TokenClass.RAFSI, buf[pos:pos + rafsi_len])
                pos = pos + rafsi_len
                mode = T.AFTER_RAFSI
                continue
            # Possible input from here:
            # - CCVC(.*)
            # - CVCC(.*)
            if pos + 4 > len(buf):
                handler(TokenClass.RAFSI, buf[pos:])
                break
            # Possible input from here:
            # - CCVC.(.*)
            # - CVCC.(.*)
            ch5 = buf[pos + 4] if pos + 4 < len(buf) else '='
            # Try 5-letter rafsi (=gismu)
            if (ch5 in V) and is_likely_rafsi_break_start(buf, pos + 5):
                handler(TokenClass.GISMU, buf[pos:pos + 5])
                pos = pos + 5
                mode = T.AFTER_RAFSI
                continue
            # Try 4-letter rafsi
            if is_likely_rafsi_break_start(buf, pos + 4):
                handler(TokenClass.RAFSI, buf[pos:pos + 4])
                pos = pos + 4
                mode = T.AFTER_RAFSI
                continue
            # it's a 3-letter rafsi
            handler(TokenClass.RAFSI, buf[pos:pos + 3])
            pos = pos + 3
            mode = T.AFTER_RAFSI
            continue

        if T.AFTER_RAFSI == mode:
            next_pos = re_token(buf, pos, re_hyphen, handler=None)
            if next_pos > pos:
                # Distinguish 'r/n/l' as a hyphen vs rafsi begin
                hy_ch = buf[next_pos - 1]
                if hy_ch != ',':
                    next_ch = buf[next_pos] if next_pos < len(buf) else 'a'
                    if next_ch in V:
                        next_pos -= 1
            if next_pos > pos:
                handler(TokenClass.HYPHEN, buf[pos:next_pos])
                pos = next_pos
            mode = T.AFTER_HYPHEN
            continue

        if T.TRY_CMAVO == mode:
            next_pos = pos
            while T.UNKNOWN != mode:
                if pos + 2 < len(buf):
                    ch2 = buf[pos + 1]
                    ch3 = buf[pos + 2]
                    if ((("'" == ch2) and ('y' == ch3))
                            or (('b' == ch2) and ('u' == ch3))):
                        next_pos = pos + 3
                        break
                if 'y' == ch:
                    next_pos = pos + 1
                    break
                if (pos + 1 < len(buf)) \
                        and (buf[pos + 1] == 'y') \
                        and (ch in C):
                    next_pos = pos + 2
                    break
                next_pos = re_token(buf, pos, re_cmavo, handler=None)
                if next_pos > pos:
                    break
                mode = T.UNKNOWN
            if T.UNKNOWN != mode:
                cmavo = buf[pos:next_pos]
                handler(TokenClass.CMAVO, cmavo)
                pos = next_pos
                mode = (T.SKIP if (cmavo != 'zoi' and cmavo != "la'o")
                        else T.QUOTE)
            continue

        if T.QUOTE == mode:
            mode = T.SKIP
            pos = re_token(buf, pos, re_skip,
                           lambda s: handler(TokenClass.SKIP, s))
            dot_pos = buf.find('.', pos)
            if dot_pos <= pos:
                continue
            qpos = dot_pos + 1
            qtoken = buf[pos:qpos]
            handler(TokenClass.QUOTE_TOKEN, qtoken)
            pos = qpos
            qtoken = '.' + qtoken
            qpos = buf.find(qtoken, pos)
            if -1 == qpos:
                continue
            handler(TokenClass.QUOTATION, buf[pos:qpos])
            pos = qpos + len(qtoken)
            handler(TokenClass.QUOTE_TOKEN, buf[qpos:pos])
            continue

        if ('[' == ch) and ('[MASK]' == buf[pos:pos + 6]):
            handler(TokenClass.MARKUP, '[MASK]')
            pos += 6
            mode = T.SKIP
            continue

        # Unknown
        handler(TokenClass.UNKNOWN, ch)
        pos += 1
        mode = T.SKIP


# The function `is_word()` doesn't care for word ends,
# it returns `True` for the text like `mi klama`.
# However, thanks to the logic in the state machine,
# after `mi` not parsed as rafsi, it will be re-tried as cmavo.
def is_word(buf, pos):
    is_after_c = False
    n_left = 5
    while n_left and pos < len(buf):
        ch = buf[pos]
        if ch in C:
            if is_after_c:
                return True
            is_after_c = True
        elif (ch != 'y') and (ch != ','):
            is_after_c = False
            if "'" == ch:
                n_left += 1
        pos += 1
        n_left -= 1
