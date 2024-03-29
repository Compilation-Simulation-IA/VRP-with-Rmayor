from my_ast import *
from errors import SyntaticError
from utils import find_column

from tokens import tokens
import os
import ply.yacc as yacc

from logger import log
from lexer import RmayorLexer
from tokens import tokens


class Parser:
    def __init__(self,lexer=None):
        self.lexer = lexer if lexer else RmayorLexer()
        self.outputdir = '.'
        self.tokens = tokens
        self.errors = False
        self.string=""
        self.parser = yacc.yacc(start='program',
                                module=self,
                                outputdir=self.outputdir,
                                optimize=1,
                                debuglog=log,
                                errorlog=log)

    def parse(self, program, debug=True):
        self.errors = False
        return self.parser.parse(program, self.lexer.lexer, debug=log)


class RmayorParser(Parser):
    
    def p_program(self, p):
        '''program :  type num map_block stops_block vehicle_type_block clients_block company_block demands_block
                | map_block stops_block vehicle_type_block clients_block company_block demands_block'''

        if p[1] == 'Simulate':
            p[0] = ProgramNode(True,p[2],p[3],p[4],p[5],p[6],p[7],p[8])
        else:
            p[0] = ProgramNode(False,0,p[1],p[2],p[3],p[4],p[5],p[6])
        
    def p_epsilon(self, p):
        'epsilon :'
        pass
    
    def p_map_block(self,p):
        'map_block : map ocur import string ccur'
        p[0] = MapNode(p[4])
    
    def p_stops_block(self, p):
        'stops_block : stops ocur stop_declarations ccur'
        p[0] = StopsNode(p[3])
        
    def p_stop_declarations(self, p):
        '''stop_declarations : stop_declaration stop_declarations
                         | epsilon'''
        if len(p) == 2:
            p[0] = []
        else:
            p[0] = [p[1]] + p[2]
    
    def p_stop_declaration(self, p):
        'stop_declaration : id opar address colon string comma people colon num cpar'
        p[0] = StopDeclarationNode(p[1], p[5], p[9])
    
    def p_vehicle_type_block(self, p):
        'vehicle_type_block : vehicle_type ocur vehicle_type_declarations ccur'
        p[0] = VehicleTypeNode(p[3])
    
    def p_vehicle_type_declarations(self, p):
        '''vehicle_type_declarations : vehicle_type_declaration
                                  | vehicle_type_declaration vehicle_type_declarations'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]
        
    def p_vehicle_type_declaration(self, p):
        'vehicle_type_declaration : id opar miles colon num comma capacity colon num cpar'
        p[0] = VehicleTypeDeclarationNode(p[1], p[5], p[9])
    
    def p_clients_block(self, p):
        'clients_block : clients ocur client_declarations ccur'
        p[0] = ClientsNode(p[3])
    
    def p_client_declarations(self, p):
        '''client_declarations : client_declaration
                            | client_declaration client_declarations'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]
        
    def p_client_declaration(self, p):
        'client_declaration : id opar name colon string comma stops_list colon opar stops_id cpar comma depot colon id cpar'
        p[0] = ClientDeclarationNode(p[1], p[5], p[10],p[15])
    
    def p_stops_id(self, p):
        '''stops_id : stops_id comma id
                    | id'''
        if len(p) < 3:
                p[0]= [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_company_block(self, p):
        'company_block : company ocur budget colon num depot opar address colon string cpar company_declarations ccur'
        p[0] = CompanyBlockNode(p[5],p[10], p[12])

    
    def p_company_declarations(self, p):
        '''company_declarations : id id colon num
                                     | id id colon num company_declarations'''
        if len(p) == 5:
            p[0] = [CompanyDeclarationNode(p[1],p[2],p[4])]
        else:
            p[0] = [CompanyDeclarationNode(p[1],p[2],p[4])]+ p[5]
          
    def p_demands_block(self, p):
        '''demands_block : demands ocur feature_list ccur'''
        p[0] = DemandsNode(p[3])

    def p_feature_list(self, p):
        '''feature_list : epsilon
                        | multiexpr feature_list
                        | def_func feature_list'''
        p[0] = [] if len(p) == 2 else [p[1]] + p[2]

    def p_feature_list_error(self, p):
        'feature_list : error feature_list'
        p[0] = [p[1]] + p[2]

  
    def p_def_func(self, p):
        '''def_func : func id opar formals cpar colon type ocur multiexpr out atom ccur'''
        p[0] = FuncDeclarationNode(p.slice[2], p[4], p.slice[7], p[9],p[11])

    def p_def_func_error(self, p):
        '''def_func : func error opar formals cpar colon type ocur multiexpr ccur
                    | func id opar error cpar colon type ocur multiexpr ccur
                    | func id opar formals cpar colon error ocur multiexpr ccur
                    | func id opar formals cpar colon type ocur error ccur'''
        p[0] = ErrorNode()

    def p_formals(self, p):
        '''formals  : param_list
                    | param_list_empty
        '''
        p[0] = p[1]

    def p_param_list(self, p):
        '''param_list : param
                      | param comma param_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_param_list_error(self, p):
        '''param_list : error comma param_list'''
        p[0] = [ErrorNode()]

    def p_param_list_empty(self, p):
        'param_list_empty : epsilon'
        p[0] = []

    def p_param(self, p):
        'param : id colon type'
        p[0] = (p.slice[1], p.slice[3])

    def p_multiexpr(self,p):
        '''multiexpr : multiexpr expr
              | expr
              | epsilon'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 0:
                p[0] = []
        else:
            p[0] = [p[1]] + [p[2]]

    def p_expr(self, p):
        '''expr : id larrow expr
                 | comp'''
        if len(p) == 4:
            p[0] = AssignNode(p.slice[1], p[3])
        else:
            p[0] = p[1]

    def p_comp(self, p):
        '''comp : comp less op
                | comp lesseq op
                | comp equal op
                | op'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '<':
            p[0] = LessNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LessEqNode(p[1], p[3])
        elif p[2] == '=':
            p[0] = EqualNode(p[1], p[3])

    def p_comp_error(self, p):
        '''comp : comp less error
                | comp lesseq error
                | comp equal error'''
        p[0] = ErrorNode()

    def p_op(self, p):
        '''op : op plus term
              | op minus term
              | term'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])

    def p_op_error(self, p):
        '''op : op plus error
              | op minus error'''
        p[0] = ErrorNode()

    def p_term(self, p):
        '''term : term star factor
                | term div factor
                | factor'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])

    def p_term_error(self, p):
        '''term : term star error
                | term div error'''
        p[0] = ErrorNode()

    def p_factor1(self, p):
        '''factor : atom
                  | opar expr cpar'''
        p[0] = p[1] if len(p) == 2 else p[2]

    def p_factor2(self, p):
        '''factor : factor dot func_call
                  | not expr
                  | func_call'''
        if len(p) == 2:
            p[0] = StaticCallNode(*p[1])
        elif p[1] == 'not':
            p[0] = NotNode(p[2], p.slice[1])
        else:
            p[0] = CallNode(p[1], *p[3])

    def p_expr_if(self, p):
        'factor : if expr then multiexpr else multiexpr fi'
        p[0] = ConditionalNode(p[2], p[4], p[6], p.slice[1])

    def p_expr_if_error(self, p):
        '''factor : if error then multiexpr else multiexpr fi
                | if expr then error else multiexpr fi
                | if expr then multiexpr else error fi
                | if expr error multiexpr else multiexpr fi
                | if expr then multiexpr error multiexpr fi
                | if expr then multiexpr else multiexpr error'''
        p[0] = ErrorNode()

    def p_expr_while(self, p):
        'factor : while expr ocur multiexpr ccur'
        
        p[0] = WhileNode(p[2], p[4], p.slice[1])

    def p_expr_while_error(self, p):
        '''factor : while error ocur multiexpr ccur
                | while expr ocur error ccur
                | while expr ocur multiexpr error
                | while expr error multiexpr ccur'''
        p[0] = ErrorNode()

    # def p_factor_list(self, p):
    #     'factor : opar items cpar'
    #     p[0] = ListNode(p[2])

    # def p_items(self, p):
    #     '''items : items comma atom
    #              | atom'''
    #     if len(p) == 2:
    #         p[0] = [p[1]]
    #     else:
    #         p[0] = p[1] + [p[3]]
    
    # def p_factor_index(self, p):
    #     'factor : factor lbracket expr rbracket'
    #     p[0] = IndexNode(p[1], p[3])

    def p_atom_num(self, p):
        'atom : num'
        p[0] = ConstantNumNode(p.slice[1])

    def p_atom_id(self, p):
        'atom : id'
        p[0] = VariableNode(p.slice[1])

    def p_atom_boolean(self, p):
        '''atom : true
                | false'''
        p[0] = ConstantBoolNode(p.slice[1])

    def p_atom_string(self, p):
        'atom : string'
        p[0] = ConstantStrNode(p.slice[1])


    def p_func_call(self, p):
        'func_call : id opar args cpar'
        p[0] = (p.slice[1], p[3])

    def p_func_call_error(self, p):
        '''func_call : id opar error cpar
                     | error opar args cpar'''
        p[0] = (ErrorNode(), ErrorNode())

    def p_args(self, p):
        '''args : arg_list
                | arg_list_empty
        '''
        p[0] = p[1]

    def p_arg_list(self, p):
        '''arg_list : expr  
                    | expr comma arg_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_arg_list_error(self, p):
        'arg_list : error arg_list'
        p[0] = [ErrorNode()]

    def p_arg_list_empty(self, p):
        'arg_list_empty : epsilon'
        p[0] = []

    def p_error(self, p):
        self.errors = True
        if p:
            self.print_error(p)
        else:
            error_text = SyntaticError.ERROR % 'EOF'
            self.string+=error_text
            column = find_column(self.lexer.lexer, self.lexer.lexer)
            line = self.lexer.lexer.lineno
            print(SyntaticError(error_text, line, column - 1))

    def print_error(self, tok):
        error_text = SyntaticError.ERROR % tok.value
        self.string +=error_text
        line, column = tok.lineno, tok.column
        print(SyntaticError(error_text, line, column))


if __name__ == "__main__":
    with open('string4.rm', 'r') as f:
        file = f.read()
    parser = RmayorParser()
    result = parser.parse(file)
