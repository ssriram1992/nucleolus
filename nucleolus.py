# %%
import gurobipy as gp
import itertools
import charFun1

# %% Utils
def toleq(a:float, b:float, tol:float=1e-6) -> bool:
    return abs(a-b)<=tol

# %%
def nucleolus(N, charFun, infoObj=None, verbose=False):
    n = len(N)
    #  Data PreProcess
    subsets = [S for i in range(n-1) for S in itertools.combinations(N, i+1) ]
    frozen = {}
    nucl = {pp:0 for pp in N}
    # The main loop
    while True:
        completed = True
        ## Given the currently frozen coalitions, identifies the minimum possible maximal excess
        M1 = gp.Model("Nucleolus-Phase1")
        M1.params.LogToConsole=False
        x = M1.addVars(N, lb=-gp.GRB.INFINITY, name="x")
        excess = M1.addVar(obj=1, lb=-gp.GRB.INFINITY, name="MaxExc")
        for pp in N: # Only interested in imputations
            x[pp].lb = charFun([pp], infoObj)
        for i,S in enumerate(subsets):
            if S in frozen:
                M1.addConstr(charFun(S, infoObj) - gp.quicksum(x[pp] for pp in S) == frozen[S], 
                name="exc-"+str(i))
            else:
                completed = False
                M1.addConstr(charFun(S, infoObj) - gp.quicksum(x[pp] for pp in S) <= excess, 
                name="exc-"+str(i)+"F")
        M1.addConstr(x.sum('*') == charFun(N, infoObj), name="TotalVal")
        ## If every coalition is frozen, then nothing left to optimize. Otherwise, go ahead.
        if not completed:
            M1.optimize()
            theta = M1.ObjVal
            for pp in N:
                nucl[pp] = x[pp].X
        else:
            break
        #  Prospective elements in the set Sigma (Notation as per Maschler's book)
        selec = (toleq(
                        theta, 
                        (charFun(S, infoObj) - gp.quicksum(x[pp] for pp in S)).getValue()
                        ) for S in subsets
                )
        # Solve another model to check which of those prospective members are definitely in Sigma
        M2 = gp.Model("Nucleolus-Phase2")
        M2.params.LogToConsole=False
        x2 = M2.addVars(N, lb=-gp.GRB.INFINITY, name="x")
        for pp in N: # Only interested in imputations
            x2[pp].lb = charFun([pp], infoObj)
        for i,S in enumerate(subsets):
            if S in frozen:
                M2.addConstr(charFun(S, infoObj) - gp.quicksum(x2[pp] for pp in S) == frozen[S], 
                name="exc-"+str(i))
            else:
                # Observe, here the RHS is the objective value obtained earlier
                M2.addConstr(charFun(S, infoObj) - gp.quicksum(x2[pp] for pp in S) <= theta, 
                    name="exc-"+str(i))
        M2.addConstr(x2.sum('*') == charFun(N, infoObj))

        for SS in itertools.compress(subsets, selec):
            # https://stackoverflow.com/questions/8312829/how-to-remove-item-from-a-python-list-in-a-loop
            # Answer by Gurney Alex - https://stackoverflow.com/a/8313120
            M2.setObjective(charFun(SS, infoObj) - gp.quicksum(x2[pp] for pp in SS))
            M2.optimize()
            if toleq(theta, M2.ObjVal):
                frozen[SS] = theta
        if verbose:
            print(frozen)
            print('----')
    return nucl
# %%
if __name__ == "__main__":
    import numpy as np
    charFun = charFun1.charFun
    
    n = 10 # Number of players
    N = [i for i in range(n)] # The players
    verbose = False

    infoObj = charFun1.addnlInfo()
    infoObj.v = {i: int((i*i-20*i +100)/10)+ np.random.randint(0, 5) for i in range(20)}
    infoObj.w = {i: int(((i%10)*(i%10)-6*(i%10))/2) + np.random.randint(0, 10) for i in range(20)}

    print(nucleolus(N, charFun, infoObj, verbose))
