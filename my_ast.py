from ply.lex import LexToken
from my_types import *

class Node:
    pass


class ProgramNode(Node):
    def __init__(self, simulate, days, map_block, stops_block, vehicle_type_block, clients_block, company_block, demands_block):
        self.simulate = simulate
        self.days = days
        self.map_block = map_block
        self.stops_block = stops_block
        self.vehicle_type_block = vehicle_type_block
        self.clients_block = clients_block
        self.company_block = company_block
        self.demands_block = demands_block
        
class MapNode(Node):
    def __init__(self, map):
        self.map = map
        
class StopsNode:
    def __init__(self, stop_declarations):
        self.stop_declarations = stop_declarations
        
    def size(self):
        return len(self.stop_declarations)

class StopDeclarationNode:
    def __init__(self, identifier, address, people):
        self.identifier = identifier
        self.address = address
        self.people = people

class VehicleTypeNode:
    def __init__(self, declarations):
        self.declarations = declarations
class VehicleTypeDeclarationNode:
    def __init__(self, identifier, miles, capacity):
        self.identifier = identifier
        self.miles = miles
        self.capacity = capacity
        self.type = CustomVehicleType(identifier, miles, capacity, (0, 0))

class ClientsNode:
    def __init__(self, client_declarations):
        self.client_declarations = client_declarations

class ClientDeclarationNode:
    def __init__(self, identifier, name, stops,depot):
        self.identifier = identifier
        self.name = name
        self.stops = stops
        self.depot = depot
        
class CompanyBlockNode:
    def __init__(self, budget, depot, company_declarations):
        self.budget = budget
        self.depot = depot
        self.company_declarations = company_declarations

class CompanyDeclarationNode:
    def __init__(self, identifier, vehicle_type, count):
        self.identifier = identifier
        self.vehicle_type = vehicle_type
        self.count = count
class DemandsNode:
        def __init__(self, demands):
            self.demands = demands
class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ErrorNode(Node):
    value = "Error"
    pass


# class ClassDeclarationNode(DeclarationNode):
#     def __init__(self, idx: LexToken, features, parent=None):
#         self.id = idx.value
#         self.pos = (idx.lineno, idx.column)
#         if parent:
#             self.parent = parent.value
#             self.parent_pos = (parent.lineno, parent.column)
#         else:
#             self.parent = None
#             self.parent_pos = (0, 0)
#         self.features = features
#         self.token = idx


class _Param:
    def __init__(self, tok):
        self.value = tok.value
        self.pos = (tok.lineno, tok.column)


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx: LexToken, params, return_type: LexToken, body, return_expr):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.params = [(pname.value, _Param(ptype)) for pname, ptype in params]
        self.type = Type.type_dict(return_type.value,self.pos)
        self.type_pos = (return_type.lineno, return_type.column)
        self.out_expr = return_expr
        self.body=body

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx: LexToken, expr=None):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.expr = expr


class AssignNode(ExpressionNode):
    def __init__(self, idx: LexToken, expr):
        if isinstance(idx, LexToken):
            self.id = idx.value
            self.pos = (idx.lineno, idx.column)
        else:
            self.id = idx
            self.pos = None
            VarDeclarationNode(idx,expr)
        self.expr = expr


class CallNode(ExpressionNode):
    def __init__(self, obj, idx: LexToken, args):
        self.obj = obj
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.args = args


class BaseCallNode(ExpressionNode):
    def __init__(self, obj, typex: LexToken, idx: LexToken, args):
        self.obj = obj
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.args = args
        self.type = typex.value
        self.type_pos = (typex.lineno, typex.column)


class StaticCallNode(ExpressionNode):
    def __init__(self, idx: LexToken, args):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.args = args


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        try:
            self.lex = lex.value
            self.pos = (lex.lineno, lex.column)
        except AttributeError:
            self.lex = lex
            self.pos = (0, 0)


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.pos = left.pos


class BinaryLogicalNode(BinaryNode):
    pass


class BinaryArithNode(BinaryNode):
    pass


class UnaryNode(ExpressionNode):
    def __init__(self, expr, tok):
        self.expr = expr
        self.pos = (tok.lineno, tok.column)


class UnaryLogicalNode(UnaryNode):
    pass


class UnaryArithNode(UnaryNode):
    pass


class WhileNode(ExpressionNode):
    def __init__(self, cond, expr, tok):
        self.cond = cond
        self.expr = expr
        self.pos = (tok.lineno, tok.column)


class ConditionalNode(ExpressionNode):
    def __init__(self, cond, stm, else_stm, tok):
        self.cond = cond
        self.stm = stm
        self.else_stm = else_stm
        self.pos = (tok.lineno, tok.column)

class OptionNode(ExpressionNode):
    def __init__(self, idx: LexToken, typex, expr):
        self.id = idx.value
        self.pos = (idx.lineno, idx.column)
        self.typex = typex.value
        self.type_pos = (typex.lineno, typex.column)
        self.expr = expr


class LetNode(ExpressionNode):
    def __init__(self, init_list, expr, tok):
        self.init_list = init_list
        self.expr = expr
        self.pos = (tok.lineno, tok.column)

    def __hash__(self):
        return id(self)


class ConstantNumNode(AtomicNode):
    pass


class ConstantBoolNode(AtomicNode):
    pass


class ConstantStrNode(AtomicNode):
    pass


class ConstantVoidNode(AtomicNode):
    def __init__(self, obj):
        super().__init__(obj)


class SelfNode(Node):
    pass


class VariableNode(AtomicNode):
    pass


class TypeNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class BinaryNotNode(UnaryArithNode):
    
    pass


class NotNode(UnaryLogicalNode):
    def __init__(self, expr, tok):
        super().expr = expr
        super().pos = (tok.lineno, tok.column)
        self.value = not expr


class PlusNode(BinaryArithNode):
    def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left+right


class MinusNode(BinaryArithNode):
    def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left - right
    


class StarNode(BinaryArithNode):
     def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left * right


class DivNode(BinaryArithNode):
     def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left / right


class LessNode(BinaryLogicalNode):
    def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left < right


class LessEqNode(BinaryLogicalNode):
    def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left <= right


class EqualNode(BinaryLogicalNode):
    def __init__(self, left, right):
        super().left = left
        super().right = right
        super().pos = left.pos
        self.value = left == right
