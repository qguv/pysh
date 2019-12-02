from tokenize import generate_tokens, untokenize
from token import *
from keyword import iskeyword
from io import StringIO

import patterns
from chars import *

def wrap_str(w):
    quote = SINGLE_QUOTE if DOUBLE_QUOTE in w and not SINGLE_QUOTE in w else DOUBLE_QUOTE
    ret = quote + w.replace(quote, '\\' + quote) + quote
    if patterns.balanced_braces(w):
        ret = 'f' + ret
    return ret

def dumps(line):
    source = list(generate_tokens(StringIO(line).readline))
    xpiled = []

    in_func = False
    first_arg = False
    for i, tok in enumerate(source):
        next_tok = source[i+1] if len(source) > i + 1 else None
        overnext_tok = source[i+2] if len(source) > i + 2 else None

        if tok.type == NAME:
            # keyword: don't quote, and break out of current call
            # TODO: True, False, None are valid arguments
            if iskeyword(tok.string):
                if in_func:
                    xpiled.append((RPAR, ')'))
                    in_func = first_arg = False
                xpiled.append((tok.type, tok.string))
                continue

            # variable
            if len(tok.string) > 1 and tok.string[0] == '$':
                if in_func:
                    if first_arg:
                        first_arg = False
                    else:
                        xpiled.append((COMMA, ','))
                xpiled.append((NAME, tok.string))
                continue

            if not in_func:

                # begin no-args func call
                if next_tok and overnext_tok and next_tok.type == LPAR and overnext_tok.type == RPAR:
                    xpiled.append((NAME, tok.string))
                    continue

                # begin func call with args
                # TODO: True, False, None are valid arguments
                if next_tok and next_tok.type in (NAME, NUMBER) and not iskeyword(next_tok.string):
                    in_func = True
                    xpiled.extend([
                        (NAME, tok.string),
                        (LPAR, '('),
                    ])
                    continue

            # string
            if in_func:
                if first_arg:
                    first_arg = False
                else:
                    xpiled.append((COMMA, ','))
            xpiled.append((STRING, wrap_str(tok.string)))
            continue

        # numeric function argument
        if tok.type == NUMBER:
            if in_func:
                if first_arg:
                    first_arg = False
                else:
                    xpiled.append((COMMA, ','))
            xpiled.append((NUMBER, tok.string))
            continue

        if tok.type == LPAR:
            xpiled.append((tok.type, tok.string))
            continue

        if in_func:
            xpiled.append((RPAR, ')'))
            in_func = first_arg = False
        xpiled.append((tok.type, tok.string))
        continue

    return untokenize(xpiled)
