from errors import SemanticError, AttributesError, TypesError, NamesError
from my_types import*
from tools import Context, Scope
import visitor
from utils import is_basic_type
from my_ast import *
from agents import *
from my_visitor import Visitor
class Semantic_Check:
    
    # stops = {}
    # vehicle_types = {}
    # client = {}
    # definiciones = {}

    def __init__(self, context:Context,visitor, errors=[]):
        self.context:Context = context
        self.current_type:Type = None
        self.errors:list = errors
        self.visitor = visitor
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
        self.errors=[]
    
    @visitor.when(StopsNode)
    def visit(self, node:StopsNode,scope:Scope):
        for dec in node.stop_declarations:
            self.visit(dec,scope)
    
    @visitor.when(StopDeclarationNode)
    def visit(self, node:StopDeclarationNode,scope:Scope):
        # self.stops[node.identifier]= [node.address,node.people]
        pass
        
    @visitor.when(VehicleTypeNode)
    def visit(self, node:VehicleTypeNode,scope:Scope):
        for dec in node.declarations:
            self.visit(dec,scope)
    
    @visitor.when(VehicleTypeDeclarationNode)
    def visit(self, node:VehicleTypeDeclarationNode,scope:Scope):
        # self.vehicle_types[node.identifier]=[node.type]
        pass
    
    @visitor.when(ClientsNode)
    def visit(self, node:ClientsNode,scope:Scope):
        for dec in node.client_declarations:
            self.visit(dec,scope)
            
    @visitor.when(ClientDeclarationNode)
    def visit(self, node:ClientDeclarationNode,scope:Scope):
        for stop in node.stops:
            if stop not in self.visitor.stops:
               raise Exception("Identificador de parada no declarado: " + stop +" en "+ node.identifier)
        if node.depot not in self.visitor.stops:
            raise Exception("Identificador de deposito no declarado: " + node.depot + " en "+ node.identifier)
        elif self.visitor.stops[node.depot][1] > 0:
            raise Exception ("Deposito " + node.depot + " no puede tener clientes")
        
    @visitor.when(CompanyBlockNode)
    def visit(self, node:CompanyBlockNode,scope:Scope):
        for dec in node.company_declarations:
            self.visit(dec,scope)
            
    @visitor.when(CompanyDeclarationNode)
    def visit(self, node:CompanyDeclarationNode,scope:Scope):
        # min_capacity = int('inf')
        # max_stop = 0
        if node.vehicle_type not in self.visitor.vehicle_types:
            raise TypeError("Tipo de vehiculo no declarado: "+ node.vehicle_type)
        #     min_capacity = min(min_capacity,dec.type.capacity)
        # for stop in self.stops:
        #     max_stop = max(max_stop,stop[2])
        # if max_stop>min_capacity:
        #     raise Exception("La parada de mayor cantidad es mayor que la capacidad del menor vehiculo")

                
    @visitor.when(DemandsNode)
    def visit(self, node:DemandsNode,scope:Scope):
        i=0
        for dec in node.demands:
            if type(node.demands[i]) is list:
                for dec1 in node.demands[i]:
                    self.visit(dec1,scope)
            else: 
                self.visit(dec,scope)
            i+=1

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode,scope:Scope):
        new_scope = scope.create_child()
        # new_scope.functions = [m for m in scope.functions]
        if node.type is None:
            raise TypeError("Tipo de retorno desconocido")

        for p in node.params:
            self.visit(p[1],new_scope)
            new_scope.locals=p[0]
        if type(node.body) is list:
            for dec in node.body:
                self.visit(dec,new_scope)
        else: self.visit(dec,new_scope)
        self.visit(node.out_expr,new_scope)
  
        
    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode,scope:Scope):
        evaluated_args = [self.visit(arg) for arg in node.args]
        if node.id not in self.visitor.definiciones:
              SemanticError("La función no existe")
        else:
            for i in evaluated_args:
                if type(evaluated_args[i])!=type(self.visitor.definiciones[1][i]):
                    SemanticError("Un argumento no es del tipo deseado")
        #     Visitor.definiciones[node.id,scope](*evaluated_args)
        # else:
              
    
    # def _get_type(self, ntype, pos):
    #     try:
    #         return self.context.get_type(ntype, pos)
    #     except SemanticError as e:
    #         self.errors.append(e)
    #         return ErrorType()
        
    # def copy_scope(self, scope:Scope, parent:Type):
    #     if parent is None:
    #         return
    #     for attr in parent.attributes.values():
    #         if scope.find_variable(attr.name) is None:
    #             scope.define_attribute(attr)
    #     self.copy_scope(scope, parent.parent)
    
    # @visitor.when(VarDeclarationNode)
    # def visit(self, node:VarDeclarationNode, scope:Scope):
       
    #     try:
    #         vtype = self.context.get_type(node.type, node.pos)
    #     except SemanticError:
    #         error_text = TypesError.UNDEFINED_TYPE_LET % (node.type, node.id)
    #         self.errors.append(TypesError(error_text, *node.type_pos))
    #         vtype = ErrorType()

    #     vtype = self._get_type(node.type, node.type_pos)
    #     var_info = scope.define_variable(node.id, vtype)
       
    #     if node.expr is not None:
    #         self.visit(node.expr, scope)
    #     else:
    #         self._define_default_value(vtype, node)
            
        
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        self.visit(node.expr, scope)

    # @visitor.when(LetNode)
    # def visit(self, node:LetNode, scope:Scope):
    #     n_scope = scope.create_child()
    #     scope.expr_dict[node] = n_scope
    #     for init in node.init_list:
    #         self.visit(init, n_scope)
        
    #     self.visit(node.expr, n_scope)

    #no necesario
    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

     
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, scope:Scope):
        self.visit(node.expr, scope)
     

    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        if node.lex in self.visitor.stops or node.lex in self.visitor.clients or node.lex=="clients" or node.lex=="stops":
            return
        if node.lex not in self.visitor.variables:
            SemanticError("Variable no inicializada")
        elif self.visitor.variables[node.lex][1]!=scope.index and node.lex not in scope.locals:
            SemanticError("Variable no definida en este ambito")

    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope):
        self.visit(node.cond, scope)
        self.visit(node.expr, scope)


    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        self.visit(node.cond, scope)
        self.visit(node.stm, scope)
        self.visit(node.else_stm, scope)
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        self.visit(node.obj, scope)
        args=[]
        for arg in node.args:
            args.append(self.visit(arg, scope))
        #self.definiciones[node.id](*args)


    # @visitor.when(BaseCallNode)
    # def visit(self, node:BaseCallNode, scope:Scope):
    #     self.visit(node.obj, scope)
    #     for arg in node.args:
    #         self.visit(arg, scope)
    

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        if node.id =="stops":
                if type(node.args) is not int:
                    SemanticError("Indice desconocido")
        elif node.id in self.visitor.stops:
                if node.args!='address' and node.args!='people':
                    SemanticError("Indice desconocido")
        if node.id =="clients":
                if type(node.args) is not int:
                    SemanticError("Indice desconocido")
        elif node.id in self.visitor.clients:
                if node.args!='name' and node.args!='stops_list' and node.args!='depot':
                    SemanticError("Indice desconocido")

       
        if node.id not in self.visitor.definiciones and node.id not in IOType.methods:
            SemanticError("Se esta llamando a una funcion no declarada")
            
        # args=[]
        # for arg in node.args:
        #     args.append(self.visit(arg, scope))
        #     if args[0] == []:
        #         args = [arg.lex]
        # if self.current_type.name == 'IO':
        #         if node.id != 'out_string' and node.id != 'out_int':
        #             raise SemanticError("No se reconoce el metodo IO: "+node.id)

    # @visitor.when(OptionNode)
    # def visit(self, node:OptionNode, scope:Scope):
    #     try:
    #         typex = self.context.get_type(node.typex, node.type_pos)
    #     except TypesError:
    #         error_txt = TypesError.CLASS_CASE_BRANCH_UNDEFINED % node.typex
    #         self.errors.append(TypesError(error_txt, *node.type_pos))
    #         typex = ErrorType()

    #     scope.define_variable(node.id, typex)
    #     self.visit(node.expr, scope)
         