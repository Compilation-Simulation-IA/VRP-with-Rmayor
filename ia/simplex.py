from scipy.optimize import linprog

#c = [10,10,10,12,12,12,9,9,9,8,8,8,10,10,10]
#A = [[-10,-12,-9,-8,-10,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,-10,-12,-9,-8,-10,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,-10,-12,-9,-8,-10], [-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,-1,-1,-1,-1,-1,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1],[1 for i in range(15)],[-1 for i in range(15)]]
#b = [-7,-8,-5,-1,-1,-1,5,0]


def simplex(c,A,b):
    bound = (0,1)
    res = linprog(c, A_ub=A, b_ub=b, bounds=bound)
    return res.x



    
