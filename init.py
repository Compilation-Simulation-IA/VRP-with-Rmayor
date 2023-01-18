
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


def start_visitor(file):
        string=""
        parser = RmayorParser()
        ast = parser.parse(file)
        string=parser.string
        if string!='':
                return string+'\n'

        builder = Visitor(Context(),string)
        builder.visit(ast)
        checker = Semantic_Check(Context(),builder)
        checker.visit(ast)
        for i in checker.errors:
                string+=i.text
                if string!='':
                   string+='\n'
        if string !='':
                return string
        executor = Execute(Context(),builder,string)
        executor.visit(ast)
        for i in executor.errors:
                string+=i.text
                if string!='':
                        string+='\n'
        if string =='':
                string+=executor.string+'\n'
        
        fi=''
        with open('30_simulations.txt', 'r') as f:
              fi = f.read()
        string+=fi
        return string
