from errors import SemanticError, AttributesError, TypesError, NamesError
from my_types import *
from tools import Context, Scope
import visitor
from utils import is_basic_type
from my_ast import *
from  generate import Generator 
from agents import *
from my_visitor import Visitor

class Execute:

    def __init__(self, context:Context, errors=[]):
        self.context:Context = context
        self.errors:list = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        self.visit(node.stops_block())
        self.visit(node.vehicle_type_block)
        self.visit(node.clients_block)
        self.visit(node.company_block)
        self.visit(node.demands_block)
        self.errors=[]
    
    @visitor.when(StopsNode)
    def visit(self, node:StopsNode):
        self.visit(node.stop_declarations)
    
    @visitor.when(StopDeclarationNode)
    def visit(self, node:StopDeclarationNode,scope:Scope):
        pass
        
    @visitor.when(VehicleTypeNode)
    def visit(self, node:VehicleTypeNode,scope:Scope):
        for dec in node.declarations:
            self.visit(dec,scope)
    
    @visitor.when(VehicleTypeDeclarationNode)
    def visit(self, node:VehicleTypeDeclarationNode):
        pass
    
    @visitor.when(ClientsNode)
    def visit(self, node:ClientsNode):
        pass
            
    @visitor.when(ClientDeclarationNode)
    def visit(self, node:ClientDeclarationNode):
        pass
        
    @visitor.when(CompanyBlockNode)
    def visit(self, node:CompanyBlockNode):
        for dec in node.vehicle_declarations:
            self.visit(dec)
            
    @visitor.when(CompanyDeclarationNode)
    def visit(self, node:CompanyDeclarationNode):
        pass

                
    @visitor.when(DemandsNode)
    def visit(self, node:DemandsNode,scope:Scope):
        for dec in node.demands:
            self.visit(dec,scope)
    #   if Visitor.simulate:
    #      gen = Generator(self.vehicles,self.clients,self.depot,self.days,self.budget,self.map)
    #      gen.generate_simulation()
        pass

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode,scope:Scope):
        pass
  
        
    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode,scope:Scope):
        self.definiciones[node.id](*node.args)
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope:Scope):
       pass
            
        
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        Visitor.variables[node.id]=self.visit(node.expr, scope)

    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

     
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, scope:Scope):
        self.visit(node.expr, scope)
     

    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        pass


    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope): 
        while self.visit(node.cond, scope):
            self.visit(node.expr, scope)


    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        if self.visit(node.cond, scope):
            self.visit(node.stm, scope)
        else: self.visit(node.else_stm, scope)
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        self.visit(node.obj, scope)
        args=[]
        for arg in node.args:
            args.append(self.visit(arg, scope))
        return self.definiciones[node.id](*args)

    

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        args=[]
        for arg in node.args:
            args.append(self.visit(arg, scope))
            if args[0] == []:
                args = [arg.lex]
        if self.current_type.name == 'IO':
                if node.id == 'out_string':
                    self.current_type.out_string(args)
                    return
                if node.id == 'out_int':
                    self.current_type.methods['out_int'](args)
                    return
        return self.definiciones[node.id](*args)

    @visitor.when(OptionNode)
    def visit(self, node:OptionNode, scope:Scope):
        pass
    
    @visitor.when(ConstantNumNode)
    def visit(self, node:ConstantNumNode, scope:Scope):
        return float(node.lex)

    @visitor.when(ConstantStrNode)
    def visit(self, node:ConstantStrNode, scope:Scope):
        return str(node.lex)
    
    @visitor.when(NotNode)
    def visit(self, node:NotNode, scope:Scope):
        return node.value
    
    @visitor.when(PlusNode)
    def visit(self, node:PlusNode, scope:Scope):
        return node.value

    @visitor.when(MinusNode)
    def visit(self, node:MinusNode, scope:Scope):
        return node.value
    
    @visitor.when(StarNode)
    def visit(self, node:StarNode, scope:Scope):
        return node.value

    @visitor.when(DivNode)
    def visit(self, node:DivNode, scope:Scope):
        return node.value
    
    @visitor.when(LessNode)
    def visit(self, node:LessNode, scope:Scope):
        return node.value
    
    @visitor.when(LessEqNode)
    def visit(self, node:EqualNode, scope:Scope):
        return node.value