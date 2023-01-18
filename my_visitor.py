

from errors import SemanticError, AttributesError, TypesError, NamesError
from my_types import *
from tools import Context, Scope
import visitor
from utils import is_basic_type
from my_ast import *
# from  generate import Generator 
from agents import *


class Visitor:
   
    graph=None
    map=""
    budget=0
    name=""
    stops={}
    vehicles_count={}
    clients={}
    days=1
    depot=""
    vehicle_types={}
    definiciones = {}
    simulate=False
    variables ={}
    calls={}
    def __init__(self, context:Context, errors=[]):
        self.context:Context = context
        # self.current_type:Type = None
        self.errors:list = errors
        self.graph=None
        self.map=""
        self.budget=0
        self.name=""
        self.stops={}
        self.vehicles_count={}
        self.clients={}
        self.days=1
        self.depot=""
        self.vehicle_types={}
        self.definiciones = {}
        self.simulate=False
        self.variables ={}
        self.calls={}
    
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode,scope:Scope=Scope()):
        #self.context = Context()
        # self.context.types['String'] = StringType()
        # self.context.types['Int'] = IntType()
        # self.context.types['Object'] = ObjectType()
        # self.context.types['Bool'] = BoolType()
        # self.context.types['SELF_TYPE'] = SelfType()
        # self.context.types['IO'] = IOType()
        self.days=node.days
        self.simulate=node.simulate
        self.map = node.map_block.map
        self.visit(node.stops_block,scope)
        self.visit(node.vehicle_type_block,scope)
        self.visit(node.clients_block,scope)
        self.visit(node.company_block,scope)
        self.visit(node.demands_block,scope)
        
    
    @visitor.when(StopsNode)
    def visit(self, node:StopsNode,scope:Scope):
        for dec in node.stop_declarations:
            self.visit(dec,scope)
        
    @visitor.when(StopDeclarationNode,)
    def visit(self, node:StopDeclarationNode,scope:Scope):
        self.stops[node.identifier]=[node.address, node.people]
        pass
        
    @visitor.when(VehicleTypeNode)
    def visit(self, node:VehicleTypeNode,scope:Scope):
        for dec in node.declarations:
            self.visit(dec,scope)
    
    @visitor.when(VehicleTypeDeclarationNode)
    def visit(self, node:VehicleTypeDeclarationNode,scope:Scope):
        self.vehicle_types[node.identifier]=[node.type,node.capacity,node.miles]
        pass
    
    @visitor.when(ClientsNode)
    def visit(self, node:ClientsNode,scope:Scope):
        for dec in node.client_declarations:
            self.visit(dec,scope)
            
    @visitor.when(ClientDeclarationNode)
    def visit(self, node:ClientDeclarationNode,scope:Scope):
       self.clients[node.identifier]=[node.name, node.stops, node.depot]
       pass
        
    @visitor.when(CompanyBlockNode)
    def visit(self, node:CompanyBlockNode,scope:Scope):
        self.budget=node.budget
        self.depot=node.depot
        for dec in node.company_declarations:
            self.visit(dec,scope)
            
    @visitor.when(CompanyDeclarationNode)
    def visit(self, node:CompanyDeclarationNode,scope:Scope):
            id = node.identifier
            self.vehicles_count[id]=[node.vehicle_type, node.count]
            
    @visitor.when(DemandsNode)
    def visit(self, node:DemandsNode,scope:Scope):
            i=0
            for dec in node.demands:
                if type(node.demands[i]) is list:
                    for dec1 in node.demands[i]:
                        self.visit(dec1,scope)
                else: self.visit(dec,scope)
                i+=1
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode,scope:Scope):
        params = node.params
        scope.locals=params
        new_scope=scope.create_child()
        if type(node.body) is list:
            for dec in node.body:
                self.visit(dec,new_scope)
        else: self.visit(node.body,new_scope)
        self.definiciones[node.id]= [node,node.body,node.params,node.out_expr,node.type]
        
    # @visitor.when(StaticCallNode)
    # def visit(self, node:StaticCallNode):
    #     for arg in node.args:
    #         self.visit(arg)
        
    
    # @visitor.when(VarDeclarationNode)
    # def visit(self, node:VarDeclarationNode):
    #     self.visit(node.expr)
    #     self.variables[node.id]=node.expr
            
        
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode,scope:Scope):
        self.visit(node.expr,scope.create_child())
        if node.id not in self.variables: 
            self.variables[node.id]=[node.expr,scope.index]
        else: self.variables[node.id]=[node.expr,self.variables[node.id][1]]

    # @visitor.when(LetNode)
    # def visit(self, node:LetNode, scope:Scope):
    #     n_scope = scope.create_child()
    #     scope.expr_dict[node] = n_scope
    #     for init in node.init_list:
    #         self.visit(init, n_scope)
        
    #     self.visit(node.expr, n_scope)

    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode,scope:Scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)

     
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode,scope:Scope):
        self.visit(node.expr,scope)
     

    @visitor.when(VariableNode)#Si es none entonces devolver None
    def visit(self, node:VariableNode,scope:Scope):
        # try:
        #     return self.current_type.get_attribute(node.lex, node.pos).type
        # except AttributesError:
        #     # if not scope.is_defined(node.lex):
        #     #     error_text = NamesError.VARIABLE_NOT_DEFINED %(node.lex)
        #     #     self.errors.append(NamesError(error_text, *node.pos))
        #     #     vinfo = scope.define_variable(node.lex, ErrorType(node.pos))
        #     # else:
        #     #     vinfo = scope.find_variable(node.lex)
        #     # return vinfo.type
        #     if not self.variables[node.lex]:
        #         error_text = NamesError.VARIABLE_NOT_DEFINED %(node.lex)
        #         self.errors.append(NamesError(error_text, *node.pos))
        pass


    @visitor.when(WhileNode)
    def visit(self, node:WhileNode,scope:Scope):
        self.visit(node.cond,scope)
        self.visit(node.expr,scope.create_child())


    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode,scope:Scope):
        self.visit(node.cond,scope)
        self.visit(node.stm,scope.create_child())
        self.visit(node.else_stm,scope.create_child())
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode,scope:Scope):
        self.visit(node.obj,scope)
        for arg in node.args:
            self.calls[node.id,scope.index] = [arg.lex]
        # self.definiciones[node.id](*args)


    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        if node.id in self.stops or node.id in self.clients or node.id=="clients" or node.id=="stops":
            pass
        args={}
        for arg in node.args:
            self.visit(arg,scope)
            self.calls[node.id,scope.index] = [arg]
        if node.args == []:
            self.calls[node.id,scope.index]=[]
        # if self.current_type.name == 'IO':
        #         if node.id == 'out_string':
        #             self.current_type.out_string(args)
        #         elif node.id == 'out_int':
        #             self.current_type.methods['out_int'](args)
        # else:
        #     self.definiciones[node.id](*args)

    # @visitor.when(OptionNode)
    # def visit(self, node:OptionNode,scope:Scope):
    #     try:
    #         typex = self.context.get_type(node.typex, node.type_pos)
    #     except TypesError:
    #         error_txt = TypesError.CLASS_CASE_BRANCH_UNDEFINED % node.typex
    #         self.errors.append(TypesError(error_txt, *node.type_pos))
    #         typex = ErrorType()

    #     # scope.define_variable(node.id, typex)
    #     self.visit(node.expr,scope)