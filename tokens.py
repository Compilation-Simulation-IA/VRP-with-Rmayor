reserved = {
    'class': 'class',
    'agents': "agents",
    'environment': "environment",
    'map': "map",
    'create': "create",
    'as': "as",
    'if': "if",
    'fi': 'fi',
    'then': "then",
    'else': "else",
    'while': "while",
    'loop': 'loop',
    'pool': 'pool',
    'false': 'false',
    'new': 'new',
    'of': 'of',
    'not': 'not',
    'true': 'true',
    'let': 'let',
    'in': 'in',
    'func': 'func',
    'isvoid': 'isvoid',
    'inherits': 'inherits',

    'stages': 'stages',
    'depot': 'depot',         # DEPOT
    'bus_stop': 'bus_stop',      # BUS_STOP
    'company': 'company',       # COMPANY
    'vehicle': 'vehicle',       # VEHICLE
    'client': 'client',        # CLIENT
    'firm': 'firm',          # FIRM
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
    'rarrow',   # '->'
    'arroba',   # '@'
    'nox',          # ~

    'plus',         # +
    'minus',        # -
    'star',     # \*
    'div',       # /
    'mod',       # %
    'equal',     # =
    'lesseq',       # <=
    'less',         # <




    'and',          # &
    'or',           # |




    # 'vehicle_type',  # VEHICLE TYPE



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
