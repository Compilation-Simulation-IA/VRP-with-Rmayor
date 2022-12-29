from cmp.pycompiler import Symbol, NonTerminal, Terminal, EOF, Sentence, Epsilon, Production, Grammar
from cmp.utils import ContainerSet
from cmp.utils import pprint, inspect

class AttributeProduction(Production):
    
    def __init__(self, nonTerminal, sentence, attributes):
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super(AttributeProduction, self).__init__(nonTerminal, sentence)

        self.attributes = attributes

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right


    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon

G = Grammar()
E = G.NonTerminal('E', True)
T, X, K, C, R, W = G.NonTerminals('T X K C R W')
client,company, plus, minus, to, div, opar, cpar, num = G.Terminals(' client company + - -> / ( ) num')

############################ BEGIN PRODUCTIONS ############################   Revisar heredados y sintetizados
# E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]
# E %= K + C, lambda h,s: s[2], None, lambda h,s: s[1]
# E %= K + R, lambda h,s: s[2], None, lambda h,s: s[1]
# E %= W + T + X, lambda h,s: s[2], None, lambda h,s: s[1],lambda h,s: s[2]
# #                                                                         
# X %= plus + T + X, lambda h,s:s[3], None, None, lambda h,s:h[0]+s[2]      
# X %= minus + T + X, lambda h,s:s[3], None, None, lambda h,s:h[0]-s[2]     
# X %= G.Epsilon, lambda h,s:h[0]                                           
# #
# T %= client,  lambda h,s:s[1], None        
# #                                                                         
# C %= plus + C + K, lambda h,s:s[3], None, None, lambda h,s:h[0]*s[2]      
# C %= G.Epsilon, lambda h,s:h[0]                                           
# #                                                                         
# K%= company,  lambda h,s:s[1], None 
# #
# R%= div + num, lambda h,s:s[1]/s[2], None, None
# #
# W %= K + to, lambda h,s:s[1], None, None                                  
############################# END PRODUCTIONS #############################

print(G)

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.contains_epsilon = True
    else:
        index=1
        beta= ContainerSet()
        if alpha[0].IsTerminal:
                first_alpha.add(alpha[0])
        if alpha[0].IsNonTerminal:
                first_alpha.update(firsts[alpha[0]])
        if firsts[alpha[0]].contains_epsilon:
            if index< len(alpha):
                beta=alpha[index]
            for i in range(index+1,len(alpha)):
                beta= beta + alpha[i]
            first_alpha.hard_update(firsts[beta])
                
    # First(alpha)
    return first_alpha

    # Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)
            
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

firsts = compute_firsts(G)
print(firsts)

from itertools import islice

def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            index =0
            for Xi in alpha:
                local_change = False
                index+=1
                if Xi.IsNonTerminal:
                    follow_Xi = follows[Xi]
                    if index< len(alpha):
                        beta=alpha[index]
                        for i in range(index+1,len(alpha)):
                            beta= beta + alpha[i]
                        local_change |= follow_Xi.update(firsts[beta])
                        if firsts[beta].contains_epsilon:
                            local_change |= follow_Xi.update(follow_X)
                    else:
                        follow_Xi.update(follow_X)
                    if local_change:
                        change=True
            

    # Follow(Vn)
    return follows

follows = compute_follows(G, firsts)
print(follows)

from operator import contains


def build_parsing_table(G, firsts, follows):
    # init parsing table
    M = {}
    
    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right
       
        for t in G.terminals:
            if contains(firsts[alpha],t):
                M[X,t]=[production]
            
            if firsts[alpha].contains_epsilon and contains(follows[X],t):
                M[X,t]=[production]
        t = G.EOF
        if firsts[alpha].contains_epsilon and contains(follows[X],t):
                M[X,t]=[production]
    # parsing table is ready!!!
    return M 

M = build_parsing_table(G, firsts, follows)

print(M)

from queue import Empty


def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)
    
    
    # parser construction...
    def parser(w):
        
        stack = [G.startSymbol]
        cursor = 0
        output = []
        
        while True:
            top = stack.pop()
            a = w[cursor]
            
            if top == a:
                cursor+=1
                if stack == []:
                    break
                continue
            production = M[top,a]
            output.append(production[0])
            for i in reversed(production[0].Right):
                stack.append(i)

            if stack == []:
                break
        # left parse is ready!!!
        return output
    
    # parser is ready!!!
    return parser
    
parser = metodo_predictivo_no_recursivo(G, M)
left_parse = parser([company, to, client, plus, client, plus, client, plus, client, G.EOF])
pprint(left_parse)

######################################################PARTE 2##################################################################################

from msilib.schema import Error


class Node:
    def evaluate(self):
        raise NotImplementedError()

class ConstantNumberNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.value = float(lex)
        
    def evaluate(self):
        return self.value

class ClientNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.value = lex
        
    def evaluate(self):
        return self.value

class CompanyNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.value = lex
        self.route = []
        
    def evaluate(self):
        return self.value
        

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue=None
        rvalue=None
        if self.left is not None and self.right is not None: 
            lvalue = self.left.evaluate()
            rvalue = self.right.evaluate()
            return self.operate(lvalue, rvalue)
        elif self.left is None:
            if self.right is not None:
                return self.right.evaluate()
            raise NotImplementedError()
        else:
            return self.left.evaluate()
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

class PlusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue.append(rvalue)

class MinusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue.remove(rvalue)

# class StarNode(BinaryNode):
#     @staticmethod
#     def operate(lvalue, rvalue):
#         return lvalue*rvalue

class DivNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        companies=[]
        for i in rvalue:
            company=[]
            for j in i*len(lvalue)/rvalue:
                company.append(lvalue[j])
            companies.append(company)
        return companies

class ToNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue.route(rvalue)

E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]
E %= K + C, lambda h,s: s[2], None, lambda h,s: s[1]
E %= K + R, lambda h,s: s[2], None, lambda h,s: s[1]
E %= W + T + X, lambda h,s: s[2], None, lambda h,s: s[1],lambda h,s: s[2]
# #                                                                         
X %= plus + T + X, lambda h,s:s[3], None, None, lambda h,s:PlusNode(h[0],s[2])       
X %= minus + T + X, lambda h,s:s[3], None, None, lambda h,s:MinusNode(h[0],s[2])      
X %= G.Epsilon, lambda h,s:h[0]                                           
# #
T %= client,  lambda h,s:s[1], None        
# #                                                                         
C %= plus + C + K, lambda h,s:s[3], None, None, lambda h,s:PlusNode(h[0],s[2])      
C %= G.Epsilon, lambda h,s:h[0]                                           
# #                                                                         
K%= company,  lambda h,s:CompanyNode(s[1]), None 
# #
R%= div + num, lambda h,s:s[1]/ConstantNumberNode(s[2]), None, None
# #
W %= K + to, lambda h,s:ToNode(s[1]), None, None

from cmp.ast import get_printer
printer = get_printer(AtomicNode=ConstantNumberNode, BinaryNode=BinaryNode)