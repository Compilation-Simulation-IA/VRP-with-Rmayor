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
    def __init__(self, lexer=None):
        self.lexer = lexer if lexer else RmayorLexer()
        self.outputdir = 'comp/output_parser/'
        self.tokens = tokens
        self.errors = False
        self.parser = yacc.yacc(start='program',
                                module=self,
                                outputdir=self.outputdir,
                                optimize=1,
                                debuglog=log,
                                errorlog=log)

    def parse(self, program, debug=True):
        self.errors = False
        # tokens = self.lexer.tokenize_text(program)
        return self.parser.parse(program, self.lexer.lexer, debug=log)


class RmayorParser(Parser):
    vehicle_types = {}
    stops = {}
    client = {}
    def p_program(self, p):
        # 'program : map_block stop_block vehicle_type_block clients_block company_block demands_block'
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
        # No hay declaraciones de paradas
            p[0] = []
        else:
        # Una o más declaraciones de paradas
            p[0] = [p[1]] + p[2]
    
    def p_stop_declaration(self, p):
        'stop_declaration : id opar address colon string comma people colon num cpar'
        p[0] = StopDeclarationNode(p[1], p[5], p[9])
        self.stops[p[1]] = p[0]
    
    def p_vehicle_type_block(self, p):
        'vehicle_type_block : vehicle_type ocur vehicle_type_declarations ccur'
        p[0] = VehicleTypeNode(p[3])
    
    def p_vehicle_type_declarations(self, p):
        '''vehicle_type_declarations : vehicle_type_declaration
                                  | vehicle_type_declaration vehicle_type_declarations'''
        if len(p) == 2:
        # Una sola declaración de tipo de vehículo
            p[0] = [p[1]]
        else:
        # Múltiples declaraciones de tipo de vehículo
            p[0] = [p[1]] + p[2]
        
    def p_vehicle_type_declaration(self, p):
        'vehicle_type_declaration : id opar miles colon num comma capacity colon num cpar'
        p[0] = VehicleTypeDeclarationNode(p[1], p[5], p[9])
        self.vehicle_types[p[1]] = p[0].type
    
    def p_clients_block(self, p):
        'clients_block : clients ocur client_declarations ccur'
        p[0] = ClientsNode(p[3])
    
    def p_client_declarations(self, p):
        '''client_declarations : client_declaration
                            | client_declaration semi client_declarations'''
        if len(p) == 2:
        # Una sola declaración de cliente
            p[0] = [p[1]]
        else:
        # Múltiples declaraciones de cliente
            p[0] = [p[1]] + p[2]
        
    def p_client_declaration(self, p):
        '''client_declaration : id opar name colon string comma stops_list colon opar stops_id cpar comma depot colon id cpar
                            | id plus id'''
        if len(p) == 4:
            if p[1] not in self.client:
                raise Exception("Identificador de parada no declarado: " + p[1])
            if p[3] not in self.client:
                raise Exception("Identificador de parada no declarado: " + p[3])
            else: 
                p[0] = ClientDeclarationNode(self.client[p[1]][0], self.client[p[1]][1], self.client[p[1]][2].append(self.client[p[3]][2]),self.client[p[1]][3])
        if p[15] not in self.stops:
                # Identificador de parada no declarado
            raise Exception("Identificador de parada no declarado: " + p[1])
        else:
            stop = self.stops[p[15]]
            self.client[p[1]]=[p[1],p[5],p[10],stop]
        p[0] = ClientDeclarationNode(p[1], p[5], p[10],stop)
    
    def p_stops_id(self, p):
        '''stops_id : stops_id comma id
                    | id'''
        if len(p) < 3:
            if p[1] not in self.stops:
                # Identificador de parada no declarado
                raise Exception("Identificador de parada no declarado: " + p[1])
            else:
                stop = self.stops[p[1]]
                p[0]= [stop]
        else:
            if p[2] not in self.stops:
                # Identificador de parada no declarado
                raise Exception("Identificador de parada no declarado: " + p[3])
            else:
                stop = self.stops[p[3]]
                if len(p) == 3:
                    p[0]= [stop]
                else:
                    p[0] = p[1] + [stop]

    def p_company_block(self, p):
        'company_block : company ocur budget colon num depot opar address colon string cpar company_declarations ccur'
        p[0] = CompanyBlockNode(p[5],p[8], p[10])

    
    def p_company_declarations(self, p):
        '''company_declarations : id id colon num
                                     | id id colon num company_declarations'''
        if p[1] not in self.vehicle_types:
            # Identificador de tipo de vehículo no declarado
            raise Exception("Identificador de tipo de vehículo no declarado: " + p[1])
        else:
            # Identificador de tipo de vehículo declarado
            vehicle_type = self.vehicle_types[p[1]]
            # Crear instancia de VarDeclarationNode
            idx = LexToken()
            idx.id = p[2]
            idx.value = p[2]
            idx.type = vehicle_type
            idx.lineno= p.lineno
            idx.column=len(p[1])
            node = VarDeclarationNode(idx, vehicle_type, p[4])
            if len(p) == 5:
                # Declaración de tipo de vehículo
                p[0] = CompanyDeclarationNode(p[1],[node])
            else:
                # Múltiples declaraciones
                p[0] = [CompanyDeclarationNode(p[1],[node]), p[5]]
          
    def p_demands_block(self, p):
        '''demands_block : demands ocur feature_list ccur'''
        p[0] = DemandsNode(p[3])
    

    # def p_class_list(self, p):
    #     '''class_list : def_class class_list
    #                   | def_class'''
    #     p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    # def p_class_list_error(self, p):
    #     '''class_list : error class_list'''
    #     p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    # def p_def_class(self, p):
    #     '''def_class : class type ocur feature_list ccur semi
    #                  | class type inherits type ocur feature_list ccur semi'''
    #     if len(p) == 7:
    #         p[0] = ClassDeclarationNode(p.slice[2], p[4])
    #     else:
    #         p[0] = ClassDeclarationNode(p.slice[2], p[6], p.slice[4])

    # def p_def_class_error(self, p):
    #     '''def_class : class error ocur feature_list ccur semi
    #                  | class type ocur feature_list ccur error
    #                  | class error inherits type ocur feature_list ccur semi
    #                  | class error inherits error ocur feature_list ccur semi
    #                  | class type inherits error ocur feature_list ccur semi
    #                  | class type inherits type ocur feature_list ccur error'''
    #     p[0] = ErrorNode()

    def p_feature_list(self, p):
        '''feature_list : epsilon
                        | multiexpr feature_list
                        | def_func feature_list'''
        p[0] = [] if len(p) == 2 else [p[1]] + p[2]

    def p_feature_list_error(self, p):
        'feature_list : error feature_list'
        p[0] = [p[1]] + p[2]

    # def p_def_attr(self, p):
    #     '''def_attr : id colon type
    #                 | id colon type larrow expr'''
    #     if len(p) == 4:
    #         p[0] = AttrDeclarationNode(p.slice[1], p.slice[3])
    #     else:
    #         p[0] = AttrDeclarationNode(p.slice[1], p.slice[3], p[5])

    # def p_def_attr_error(self, p):
    #     '''def_attr : error colon type
    #                 | id colon error
    #                 | error colon type larrow expr
    #                 | id colon error larrow expr
    #                 | id colon type larrow error'''
    #     p[0] = ErrorNode()

    def p_def_func(self, p):
        'def_func : func id opar formals cpar colon type ocur multiexpr ccur'
        p[0] = FuncDeclarationNode(p.slice[2], p[4], p.slice[7], p[9])

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

    # def p_param_list_error(self, p):
    #     '''param_list : error comma param_list'''
    #     p[0] = [ErrorNode()]

    def p_param_list_empty(self, p):
        'param_list_empty : epsilon'
        p[0] = []

    def p_param(self, p):
        'param : id colon type'
        p[0] = (p.slice[1], p.slice[3])

    def p_let_list(self, p):
        '''let_list : let_assign
                    | let_assign comma let_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    # def p_let_list_error(self, p):
    #     '''let_list : error let_list
    #                 | error'''
    #     p[0] = [ErrorNode()]

    def p_let_assign(self, p):
        '''let_assign : param larrow expr
                      | param'''
        if len(p) == 2:
            p[0] = VarDeclarationNode(p[1][0], p[1][1])
        else:
            p[0] = VarDeclarationNode(p[1][0], p[1][1], p[3])

    # def p_cases_list(self, p):
    #     '''cases_list : casep semi
    #                   | casep semi cases_list'''
    #     p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    # def p_cases_list_error(self, p):
    #     '''cases_list : error cases_list
    #                   | error semi'''
    #     p[0] = [ErrorNode()]

    # def p_case(self, p):
    #     'casep : id colon type rarrow expr'
    #     p[0] = OptionNode(p.slice[1], p.slice[3], p[5])

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

    # # def p_comp_error(self, p):
    # #     '''comp : comp less error
    # #             | comp lesseq error
    # #             | comp equal error'''
    # #     p[0] = ErrorNode()

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

    # def p_op_error(self, p):
    #     '''op : op plus error
    #           | op minus error'''
    #     p[0] = ErrorNode()

    def p_term(self, p):
        '''term : term star base_call
                | term div base_call
                | base_call'''
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

    def p_base_call(self, p):
        '''base_call : factor arroba type dot func_call
                     | factor'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BaseCallNode(p[1], p.slice[3], *p[5])

    def p_base_call_error(self, p):
        '''base_call : error arroba type dot func_call
                     | factor arroba error dot func_call
        '''
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

    def p_factor3(self, p):
        '''factor : isvoid base_call
                  | nox base_call
        '''
        if p[1] == 'isvoid':
            p[0] = IsVoidNode(p[2], p.slice[1])
        else:
            p[0] = BinaryNotNode(p[2], p.slice[1])

    def p_expr_let(self, p):
        'factor : let let_list in ocur expr ccur'
        p[0] = LetNode(p[2], p[5], p.slice[1])

    # def p_expr_let_error(self, p):
    #     '''factor : let error in expr
    #             | let let_list in error
    #             | let let_list error expr'''
    #     p[0] = ErrorNode()

    # def p_expr_case(self, p):
    #     'factor : case expr of cases_list esac'
    #     p[0] = CaseNode(p[2], p[4], p.slice[1])

    # def p_expr_case_error(self, p):
    #     '''factor : case error of cases_list esac
    #             | case expr of error esac
    #             | case expr error cases_list esac
    #             | case expr of cases_list error'''
    #     p[0] = ErrorNode()

    def p_expr_if(self, p):
        'factor : if expr then expr else expr fi'
        p[0] = ConditionalNode(p[2], p[4], p[6], p.slice[1])

    # def p_expr_if_error(self, p):
    #     '''factor : if error then expr else expr fi
    #             | if expr then error else expr fi
    #             | if expr then expr else error fi
    #             | if expr error expr else expr fi
    #             | if expr then expr error expr fi
    #             | if expr then expr else expr error'''
    #     p[0] = ErrorNode()

    def p_expr_while(self, p):
        'factor : while expr ocur multiexpr ccur'
        p[0] = WhileNode(p[2], p[4], p.slice[1])
        
    # def p_expr_while_error(self, p):
    #     '''factor : while error loop expr pool
    #             | while expr loop error pool
    #             | while expr loop expr error
    #             | while expr error expr pool'''
    #     p[0] = ErrorNode()

    def p_atom_num(self, p):
        'atom : num'
        p[0] = ConstantNumNode(p.slice[1])

    def p_atom_id(self, p):
        'atom : id'
        p[0] = VariableNode(p.slice[1])

    def p_atom_new(self, p):
        'atom : new type'
        p[0] = InstantiateNode(p.slice[2])

    def p_atom_block(self, p):
        'atom : ocur block ccur'
        p[0] = BlockNode(p[2], p.slice[1])

    def p_atom_block_error(self, p):
        '''atom : error block ccur
                | ocur error ccur
                | ocur block error'''
        p[0] = ErrorNode()

    def p_atom_boolean(self, p):
        '''atom : true
                | false'''
        p[0] = ConstantBoolNode(p.slice[1])

    def p_atom_string(self, p):
        'atom : string'
        p[0] = ConstantStrNode(p.slice[1])

    def p_block(self, p):
        '''block : expr
                 | expr block'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_block_error(self, p):
        '''block : error block
                 | error'''
        p[0] = [ErrorNode()]

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

    #Error rule for syntax errors
    def p_error(self, p):
        self.errors = True
        if p:
            self.print_error(p)
        else:
            error_text = SyntaticError.ERROR % 'EOF'
            column = find_column(self.lexer.lexer, self.lexer.lexer)
            line = self.lexer.lexer.lineno
            print(SyntaticError(error_text, line, column - 1))

    def print_error(self, tok):
        error_text = SyntaticError.ERROR % tok.value
        line, column = tok.lineno, tok.column
        print(SyntaticError(error_text, line, column))


if __name__ == "__main__":
    with open('string4.rm', 'r') as f:
        file = f.read()
    # Parser()
    parser = RmayorParser()
    result = parser.parse(file)
    # print(result)
