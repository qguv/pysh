from re import compile
from chars import *

KEYWORDS = set('''
    if elif else
    from import as
    for in while
    True False None
    try except finally
    async def = := lambda del
    await return yield raise
    + - * ** / % @ & | ^
    += -= *= **= /= %= @= &= |= ^=
    == > <
    != <= >=
    and or not
    ( ) [ ]
'''.strip().split())

def _fullmatch(regex):
    return compile(regex).fullmatch

decimal = _fullmatch('[+-]?(0|[1-9](_?[0-9])*)(\.([0-9](_?[0-9])*)?)?(e[0-9](_?[0-9])*)?')
octal = _fullmatch('[+-]?0o[_0-7]+')
octal = _fullmatch('[+-]?0x[_0-9a-fA-F]+')
binary = _fullmatch('[+-]?0b[_01]+')
ident = _fullmatch('[_a-zA-Z][_a-zA-Z0-9]*')

def number(w):
    return decimal(w) or octal(w) or binary(w)

def quoted(w) -> 'end_quote' or None:
    if w[0] in QUOTE_CHARS:
        return w[0]
    if len(w) > 1 and w[0] in ('f', 'r') and w[1] in QUOTE_CHARS:
        return w[1]

def balanced_braces(w):
    imbalance = 0
    found = False
    for c in w:
        if c == '{':
            imbalance += 1
        elif c == '}':
            imbalance -= 1
            found = True
    return found and not imbalance
