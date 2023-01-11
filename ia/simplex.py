from scipy.optimize import linprog

#c = [10,10,10,12,12,12,9,9,9,8,8,8,10,10,10]
#A = [[-10,-12,-9,-8,-10,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,-10,-12,-9,-8,-10,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,-10,-12,-9,-8,-10], [-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,-1,-1,-1,-1,-1,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1],[1 for i in range(15)],[-1 for i in range(15)]]
#b = [-7,-8,-5,-1,-1,-1,5,0]
V = [8,15]
P = [5,3,2,4,5,0,0]
D=[[ 0,5,12,15,9,10,8],
    [5,0,9,11,13,11,15],
    [12,9,0,10,9,5, 10],
    [ 15,11, 10, 0,10, 8, 20],
    [9,13, 9, 10,0, 9,9],
    [10,11,5,8,9,0,40],
    [8,15,10,20,9,40,0]]

#c = [(sum(D[j]) + V[i] -P[j]) for i in range(2) for j in range(7)]
c = [(sum(D[j])) for i in range(2) for j in range(7)]
p = [(i,j) for i in range(2) for j in range(7)]
A_eq = [[0 for i in range(14)] for j in range(7)]
b_eq= [1,1,1,1,1,2,2]
A_ub=[[0 for i in range(len(c))] for j in range(len(V))]
b_ub=[8,15]

for i in range(7):
    for j in range(7):
        if i == j:
            A_eq[i][j] = 1
            A_eq[i][j+7]=1 

for i in range(len(V)):
    for j in range(7):
        if i == 0:
            A_ub[i][j]=P[j]
        else:
            A_ub[i][j+7]=P[j]



    

    
       
print(A_ub)



"""Ejemplo:
 V1 - 8
 V2 -15
 P1 -5
 P2 -3
 P3 -2
 P4 -4
 P5 -5

S1
 D1 - 0
 D2 - 5
 D3 -12
 D4 -15
 D5 -9
 D6 -10
 D7 -8

S2
 D8  -5
 D9  -0
 D10 -9
 D11 -11
 D12 -13
 D13 -11
 D14 -15

S3
 D15 -12
 D16 -9
 D17 -0
 D18 -10
 D19 -9
 D20 -5
 D21 - 10

S4
 D22 - 15
 D23 - 11
 D24 - 10
 D25 - 0
 D26 -10
 D27 - 8
 D28 - 20

S5
 D29 -9
 D30 -13
 D31 - 9
 D32 - 10
 D33 - 0
 D34 - 9
 D35 - 9

Deposito inicial
 D36 -10
 D37 -11
 D38 -5
 D39 -8
 D40 -9
 D41 -0
 D42 -40


Deposito final (cliente)
 D43 -8
 D44 -15
 D45 -10
 D46 -20
 D47 -9
 D48 -40
 D49 -0
  




"""

def simplex(c,A,b):
    bound = (0,1)
    res = linprog(c, A_ub=A, b_ub=b, bounds=bound)
    return res.x


a = {'hola':[{'s1':3},{'s2':3}], 'hi':[{'s4':3},{'s3':3}]}

#b = [stop for stop in a.values()] 



#print(linprog(c,A_eq = A_eq, b_eq = b_eq, A_ub=A_ub,b_ub=b_ub, method ='simplex'))
print(linprog(c,A_eq = A_eq, b_eq = b_eq, A_ub=A_ub,b_ub=b_ub, method ='simplex',bounds = (0,1)).x)
print(linprog(c,A_eq = A_eq, b_eq = b_eq, A_ub=A_ub,b_ub=b_ub, bounds = [0,1]).x)

    

