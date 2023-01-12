reserved = {
    'import': 'import',
    'stops_list': 'stops_list',
    'vehicle_type': 'vehicle_type',
    'clients': 'clients',
    'stops': 'stops',
    'company': 'company',
    'demands': 'demands',
    'map': "map",
    'miles': 'miles',
    'name': 'name',
    'budget': 'budget',
    'capacity': 'capacity',
    'address': 'address',
    'people': 'people',
    'depot': 'depot',
    'Simulate': 'Simulate',
    'if': "if",
    'fi': 'fi',
    'then': "then",
    'else': "else",
    'while': "while",
    'false': 'false',
    'new': 'new',
    'not': 'not',
    'true': 'true',
    'let': 'let',
    'in': 'in',
    'func': 'func',
    'isvoid': 'isvoid',
}

tokens = [
    'semi',     # '; '
    'comma',    # ', '
    'colon',    # ': '
    'dot',      # '. '
    'opar',     # '( '
    'cpar',     # ') '
    'ocur',     # '{'
    'ccur',     # '} '

    'larrow',   # '<-'
    'arroba',   # '@'
    'nox',          # ~

    'plus',         # +
    'minus',        # -
    'star',     # \*
    'div',       # /
    'equal',     # =
    'lesseq',       # <=
    'less',         # <

    'end',          # end
    'id',
    'type',
    'num',
    'string'
] + list(reserved.values())


class Token:
    def __init__(self, lex, type_, lineno, pos):
        self.lex = lex
        self.type = type_
        self.lineno = lineno
        self.pos = pos

    def __str__(self):
        return f'{self.type}: {self.lex} ({self.lineno}, {self.pos})'

    def __repr__(self):
        return str(self)
