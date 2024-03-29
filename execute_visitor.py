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
    errors=[]
    def __init__(self, context:Context, visitor,string):
        self.context:Context = context
        self.visitor=visitor
        self.errors = []
        self.string=string
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode,scope:Scope=Scope()):
        self.visit(node.stops_block,scope)
        self.visit(node.vehicle_type_block,scope)
        self.visit(node.clients_block,scope)
        self.visit(node.company_block,scope)
        self.visit(node.demands_block,scope)
    
    @visitor.when(StopsNode)
    def visit(self, node:StopsNode,scope:Scope):
        for dec in node.stop_declarations:
            self.visit(dec,scope)
    
    @visitor.when(StopDeclarationNode)
    def visit(self, node:StopDeclarationNode,scope:Scope):
        pass
        
    @visitor.when(VehicleTypeNode)
    def visit(self, node:VehicleTypeNode,scope:Scope):
        for dec in node.declarations:
            self.visit(dec,scope)
    
    @visitor.when(VehicleTypeDeclarationNode)
    def visit(self, node:VehicleTypeDeclarationNode,scope:Scope):
        pass
    
    @visitor.when(ClientsNode)
    def visit(self, node:ClientsNode,scope:Scope):
        pass
            
    @visitor.when(ClientDeclarationNode)
    def visit(self, node:ClientDeclarationNode,scope:Scope):
        pass
        
    @visitor.when(CompanyBlockNode)
    def visit(self, node:CompanyBlockNode,scope:Scope):
        for dec in node.company_declarations:
            self.visit(dec,scope)
            
    @visitor.when(CompanyDeclarationNode)
    def visit(self, node:CompanyDeclarationNode,scope:Scope):
        pass

                
    @visitor.when(DemandsNode)
    def visit(self, node:DemandsNode,scope:Scope):
        i=0
        for dec in node.demands:
            if type(node.demands[i]) is list:
                for dec1 in node.demands[i]:
                    if not dec1 is FuncDeclarationNode:
                        self.visit(dec1,scope)
            else:
                if type(dec) is not FuncDeclarationNode: 
                    self.visit(dec,scope)
            i+=1
        if self.visitor.simulate:
            gen = Generator(self.visitor.vehicles_count,self.visitor.vehicle_types,self.visitor.clients,self.visitor.stops,self.visitor.depot,self.visitor.days,self.visitor.budget,self.visitor.map)
            gen.generate_simulation()

    internals={}
    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, args ,scope:Scope):
        if len(node.params)!=len(args):
            self.errors.append(SemanticError("Cantidad incompatible de argumentos",node.pos[0],node.pos[1]))
            return
        else:
            for i, param in enumerate(node.params):
                if self.types_dict[param[1].value] != type(args[i]):
                    self.errors.append(SemanticError("Parametro con un tipo no deseado",node.pos[0],node.pos[1]))
                    return 
                else:   
                    self.internals[param[0]] =args[i]
                    scope.expr_dict[param[0]]=args[i]
        if type(node.body) is list:
            for dec in node.body:
                self.visit(dec,scope)
        else: 
                self.visit(node.body,scope)
        if node.out_expr==None:
            return None
        value=self.visit(node.out_expr,scope)
        if type(value)!=self.types_dict[node.type.name]:
            self.errors.append(SemanticError("Tipo de retorno no deseado",node.pos[0],node.pos[1]))
        self.internals={}
        return value
    types_dict={'String':str,'Int': int,'Object':object,'Bool':bool,'IO':IOType,'SELF_TYPE':SelfType,'VEHICLE_TYPE':VehicleType}
        
        
    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode,scope:Scope):
        args=[self.visit(i) for i in args]
        self.visitor.definiciones[node.id](*args)
    
    # @visitor.when(VarDeclarationNode)
    # def visit(self, node:VarDeclarationNode, scope:Scope):
    #    pass
            
    @visitor.when(ListNode)
    def visit(self,node:ListNode,scope:Scope):
        for i in node.list:
            self.visit(node.expr,scope)
    
    
    @visitor.when(ListNode)
    def visit(self,node:IndexNode,scope:Scope):
        if node.idlist == 'stops':
            return self.visitor.stops(node.index)[0]
        if node.idlist =="clients":
            return self.visitor.clients(node.index)[0]
        else: 
            if node.index>=len(self.visitor.variables[node.idlist]):
                self.errors.append(SemanticError("Indice fuera de rango"))
            return self.visitor.variables[node.idlist][node.index]

    
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        self.visitor.variables[node.id]=[self.visit(node.expr, scope),scope.index]
       # if node.id in self.internals:
        #    self.internals[node.id][0]=self.visit(node.expr, scope)
        if node.id in scope.expr_dict:
            scope.expr_dict[node.id][0] = self.visit(node.expr,scope)

    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

     
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, scope:Scope):
        self.visit(node.expr, scope)
     

    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        if node.lex in self.visitor.stops:
            return self.visitor.stops[node.lex]
        if node.lex in self.visitor.clients:
            return self.visitor.clients[node.lex]
        # for i in self.internals:
        #     if node.lex == i:
        #         return self.internals[i][0]
        for i in scope.expr_dict:
            if node.lex == i:
                return scope.expr_dict[i]
            
        return self.visitor.variables[node.lex][0]
         

    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope): 
        while self.visit(node.cond, scope):
            for dec in node.expr:
                self.visit(dec, scope)


    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        if self.visit(node.cond, scope):
            return self.visit(node.stm, scope)
        else: return self.visit(node.else_stm, scope)
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        self.visit(node.obj, scope)
        args=[]
        for arg in node.args:
            args.append(self.visit(arg, scope))
        return self.definiciones[node.id](*args)

    

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        if node.id in self.visitor.stops:
            return self.visitor.stops[node.id][node.args]
        if node.id == "stops":
            return self.visitor.stops[node.args]
        if node.id in self.visitor.clients:
            return self.visitor.clients[node.id][node.args]
        if node.id =="clients":
            return self.visitor.clients[node.args]
        args=[]
        for i in range(len(node.args)):
            args.append(self.visit(node.args[i],scope))
            
        if args==[]: 
            args = self.visitor.calls[node.id,scope.index]

        else: self.visitor.calls[node.id,scope.index]=args
        if node.id == 'out_string':
            self.string+=IOType.out_string(args[0])
            self.string+='\n'
            return
        if node.id == 'out_int':
            self.string+=IOType.out_int(args[0])
            self.string+='\n'
            return
        return self.visit(self.visitor.definiciones[node.id][0],args,scope.create_child())

    # @visitor.when(OptionNode)
    # def visit(self, node:OptionNode, scope:Scope):
    #     pass
    
    @visitor.when(ConstantNumNode)
    def visit(self, node:ConstantNumNode, scope:Scope):
        return int(node.lex)

    # @visitor.when(VariableNode)
    # def visit(self, node:VariableNode,scope:Scope):
    #     return self.visitor.variables[node.id]
    @visitor.when(ConstantStrNode)
    def visit(self, node:ConstantStrNode, scope:Scope):
        return str(node.lex)
    
    @visitor.when(NotNode)
    def visit(self, node:NotNode, scope:Scope):
        return not self.visit(node.expr,scope)
    
    @visitor.when(PlusNode)
    def visit(self, node:PlusNode, scope:Scope):
        if type(node.left) is VariableNode and node.left.lex in self.visitor.stops:
            if type(node.right) is ConstantNumNode:
                self.visitor.stops[node.left.lex][1]+=int(node.right.lex)
                return
            elif type(node.right) is VariableNode  and node.right.lex in self.visitor.stops:
                self.visitor.stops[node.left.lex][1]+=self.visitor.stops[node.right.lex][1]
                self.visitor.stops.pop(node.right.lex)
                return
        if type(node.left) is VariableNode and node.left.lex in self.visitor.clients:
            if  type(node.right) is VariableNode and node.right.lex in self.visitor.clients:
                for i in range (len(self.visitor.clients[node.right.lex][1])):
                    self.visitor.clients[node.left.lex][1].append(self.visitor.clients[node.right.lex][1][i])
                self.visitor.clients.pop(node.right.lex)
                return
        return self.visit(node.left,scope)+self.visit(node.right,scope)

    @visitor.when(MinusNode)
    def visit(self, node:MinusNode, scope:Scope):
        if type(node.left) is VariableNode and node.left.lex in self.visitor.stops:
            if type(node.right) is ConstantNumNode:
                self.visitor.stops[node.left][1]-=int(node.right.lex)
                if self.visitor.stops[node.left][1]<0:
                    self.visitor.stops[node.left][1]=0
                return
        return self.visit(node.left,scope) - self.visit(node.right,scope)
    
    @visitor.when(StarNode)
    def visit(self, node:StarNode, scope:Scope):
        return self.visit(node.left,scope) * self.visit(node.right,scope)

    @visitor.when(DivNode)
    def visit(self, node:DivNode, scope:Scope):
        if type(node.left) is VariableNode and node.left.lex in self.visitor.clients:
            if  type(node.right) is ConstantNumNode:
                if int(node.right.lex)>len(self.visitor.clients[node.left.lex][1]):
                    self.errors.append(SemanticError("No se puede fraccionar "+node.left.lex+" en "+node.right.lex))
                else:
                    parts = np.array_split(self.visitor.clients[node.left.lex][1],int(node.right.lex))
                    for i, part in enumerate(parts):
                        self.visitor.clients[f"{node.left.lex}{i}"]=[self.visitor.clients[node.left.lex][0],part,self.visitor.clients[node.left.lex][2]]
                    self.visitor.clients.pop(node.left.lex)
                    
        return self.visit(node.left,scope) / self(node.right,scope)
    
    @visitor.when(LessNode)
    def visit(self, node:LessNode, scope:Scope):
        return self.visit(node.left,scope) < self.visit(node.right,scope)
    
    @visitor.when(LessEqNode)
    def visit(self, node:LessEqNode, scope:Scope):
        return self.visit(node.left,scope) <= self.visit(node.right,scope)
    @visitor.when(EqualNode)
    def visit(self, node:EqualNode, scope:Scope):
        return self.visit(node.left,scope) == self.visit(node.right,scope)
    