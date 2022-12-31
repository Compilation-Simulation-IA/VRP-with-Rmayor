reserved = {
    'import': 'import',
    'map': 'map',
    'stop': 'stop',
    'vehicle_type': 'vehicle_type',
    'client': 'client',
    'stops': 'stops',
    'company': 'company',            
    'environment': "environment",
    'demands': 'demands',
    'main': 'main',  
    'map': "map",
    'miles': 'miles',
    'name': 'name',
    'budget': 'budget',
    'capacity': 'capacity',
    'address': 'address',
    'people': 'people',
    
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
    'osquare',  # '['
    'csquare',  # ']'
    
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
