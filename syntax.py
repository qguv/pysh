import patterns
from chars import *

def wrap_str(w):
    quote = SINGLE_QUOTE if DOUBLE_QUOTE in w and not SINGLE_QUOTE in w else DOUBLE_QUOTE
    ret = quote + w.replace(quote, '\\' + quote) + quote
    if patterns.balanced_braces(w):
        ret = 'f' + ret
    return ret

def dumps(line):
    line = line.strip()
    if not line:
        return ''

    line = line.split()
    tokens = []
    fn = None
    args = []

    while line:
        word = line.pop(0)
        level = (args if fn else tokens)

        if word in patterns.KEYWORDS:

            # write out function call (TODO DRY)
            if fn:
                if args:
                    tokens.append(fn + '(' + ', '.join(args) + ')')
                    args = []
                else:
                    tokens.append(wrap_str(fn))
                fn = None

            tokens.append(word)

        elif patterns.number(word):
            level.append(word)

        elif endquote := patterns.quoted(word):
            while line and not word.endswith(endquote):
                word += ' ' + line.pop(0)
            level.append(word)

        # ident like ${var}
        elif len(word) > 3 and word.startswith('${') and word[-1] == '}' and patterns.ident(word[2:-1]):
            level.append(word[2:-1])

        # ident like $var
        elif len(word) > 1 and word[0] == '$' and patterns.ident(word[1:]):
            level.append(word[1:])

        # ident like var()
        elif len(word) > 2 and word.endswith('()') and patterns.ident(word[:-2]):
            level.append(word)

        # ident for fn call
        elif not fn and patterns.ident(word):
            fn = word

        else:
            level.append(wrap_str(word))

    # write out function call (TODO DRY)
    if fn:
        if args:
            tokens.append(fn + '(' + ', '.join(args) + ')')
            args = []
        else:
            tokens.append(wrap_str(fn))
        fn = None

    return ' '.join(tokens)
