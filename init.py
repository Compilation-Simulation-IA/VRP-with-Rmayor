
import sys
sys.path.append("/comp/")
from errors import SemanticError, AttributesError, TypesError, NamesError
from my_types import *
from tools import Context, Scope
from my_visitor import Visitor
from execute_visitor import Execute
from semantic_checker import Semantic_Check
from utils import is_basic_type
from my_ast import *
from my_parser import RmayorParser

# with open('comp/string4.rm', 'r') as f:
#         file = f.read()
def start_visitor(file):
        parser = RmayorParser()
        ast = parser.parse(file)

        builder = Visitor(Context())
        builder.visit(ast)
        checker = Semantic_Check(Context(),builder)
        checker.visit(ast)
        executor = Execute(Context(),builder)
        executor.visit(ast)
        pass
