from errors import SemanticError, AttributesError, TypesError, NamesError
from my_types import *
from tools import Context, Scope
from my_visitor import Visitor
from utils import is_basic_type
from my_ast import *
from my_parser import RmayorParser

with open('comp/string4.rm', 'r') as f:
        file = f.read()

parser = RmayorParser()
ast = parser.parse(file)

builder = Visitor(Context())
builder.visit(ast)
