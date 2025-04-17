from pysat.formula import CNF
from pysat.solvers import Glucose42
import time
import random

start_build = time.time()
cnf=CNF()

triple_vars = {}
count=0
n=17
#create variables
for i in range(1,n+1):
    for j in range(i + 1, n+1):
        for k in range(j + 1, n+1):
            triple = (i,j,k)
            count+=1
            triple_vars[triple]=count
print(count)

#add 20 random variables
for i in range(20):
    count+=1
    r=random.choice([True,False])
    if (r):
        cnf.append([count])
    else:
        cnf.append([-1*count])
print(count)


cnf.append([triple_vars[(1,2,3)]])
for i in range(4,n+1):
    cnf.append([triple_vars[(1,2,i)]])
    cnf.append([-1*triple_vars[(2,3,i)]])

def interpolation_transitivity():
    for a in range(1,n+1):
        for b in range(a+1,n+1):
            for c in range(b+1,n+1):
                for d in range(c+1,n+1): 
                    
                    X=triple_vars[(a,b,d)]
                    Y=triple_vars[(a,c,d)]
                    W=triple_vars[(a,b,c)]
                    Z=triple_vars[(b,c,d)]

                    #transitivity
                    #((X & ~Y) >> (W & ~Z)) & ((~X & Y) >> (~W & Z))
                    #is equal to:
                    #(W | Y | ~X) & (X | Z | ~Y) & (X | ~W | ~Y) & (Y | ~X | ~Z)
                    cnf.append([W,Y,-1*X])
                    cnf.append([X,Z,-1*Y])
                    cnf.append([X,-1*W,-1*Y])
                    cnf.append([Y,-1*X,-1*Z])

                    #interpolation
                    #((W & Z) >> (X & Y)) & ((~W & ~Z) >> (~X & ~Y))
                    #is equal to:
                    #(W | Z | ~X) & (W | Z | ~Y) & (X | ~W | ~Z) & (Y | ~W | ~Z)
                    cnf.append([W,Z,-1*X])
                    cnf.append([W,Z,-1*Y])
                    cnf.append([X,-1*W,-1*Z])
                    cnf.append([Y,-1*W,-1*Z])

interpolation_transitivity()

#create clauses for every 6 points
def buildcase(p1,pn,above,below):
    literals=[]
    above.append(pn)
    below.append(pn)

    for i in range(1,len(above)-1):
        p_i =above[i]
        literals.append(-1*triple_vars[(p1,p_i,pn)])
    
    for i in range(1,len(below)-1):
        p_i =below[i]
        literals.append(triple_vars[(p1,p_i,pn)])
    
    if (len(above) > 3):
        for i in range(len(above)-2):
            literals.append(-1*triple_vars[(above[i],above[i+1],above[i+2])])
    
    if (len(below) > 3):
        for i in range(len(below)-2):
            literals.append(triple_vars[(below[i],below[i+1],below[i+2])])
    above.pop()
    below.pop()
    return literals

def iterative(p1,p2,p3,p4,p5,p6):
    above=[p1]
    below=[p1]
    for i2 in range(2):
        last2=False
        if (i2 == 1):
            above.append(p2)
            last2=True
        else:
            below.append(p2)
            last2 = False
        
        for i3 in range(2):
            last3=False
            if (i3 == 1):
                above.append(p3)
                last3=True
            else:
                below.append(p3)
                last3 = False

            for i4 in range(2):
                last4=False
                if (i4 == 1):
                    above.append(p4)
                    last4=True
                else:
                    below.append(p4)
                    last4 = False
                for i5 in range(2):
                    last5=False
                    if(i5 == 1):
                        above.append(p5)
                        last5=True
                    else:
                        below.append(p5)
                        last5=False

                    cnf.append(buildcase(p1,p6,above,below))
                    if (last5): above.pop()
                    else: below.pop()
                if (last4): above.pop()
                else: below.pop()
            if (last3): above.pop()
            else: below.pop()
        if (last2): above.pop()
        else: below.pop()

for p1 in range(1,n+1):
    for p2 in range(p1+1,n+1):
        for p3 in range(p2+1,n+1):
            for p4 in range(p3+1,n+1):
                for p5 in range(p4+1,n+1):
                    for p6 in range(p5+1,n+1):
                        iterative(p1,p2,p3,p4,p5,p6)


solver = Glucose42()
solver.append_formula(cnf)

end_build = time.time()
build_time = end_build-start_build
print(f"Built variables & clauses in {build_time} seconds")

def writeCNF():
    with open("/Users/virajnain/Desktop/code/ES_Problem/output6.cnf", "w") as file:
        file.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")
writeCNF()


start_solve=time.time()
sat=solver.solve()
end_solve=time.time()
solving_time=end_solve-start_solve
print(f"Solved in {solving_time:.4f} seconds")

def writeProof(proof):
    with open("/Users/virajnain/Desktop/code/ES_Problem/proof.cnf","w") as file:
        for s in proof:
            file.write(f"{s}\n")

if (sat):
    print("SAT\n")
    #print(solver.get_model())
else:
    print("UNSAT")
    proof=solver.get_proof()
    writeProof(proof)