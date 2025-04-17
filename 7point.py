from pysat.formula import CNF
from pysat.solvers import Glucose42
import time

start_build = time.time()
cnf=CNF()

triple_vars = {}
count=0
n=32
#create variables
for i in range(1,n+1):
    for j in range(i + 1, n+1):
        for k in range(j + 1, n+1): #store every triple (n choose 3) by its index in order of creation
            triple = (i,j,k)
            count+=1
            triple_vars[triple]=count
print(count)

cnf.append([triple_vars[(1,2,3)]])
for i in range(4,n+1):
    cnf.append([triple_vars[(1,2,i)]])
    cnf.append([-1*triple_vars[(2,3,i)]])

def interpolation_transitivity(): #build transitivity and interpolation conditions
    for a in range(1,n+1):
        for b in range(a+1,n+1):
            for c in range(b+1,n+1):
                for d in range(c+1,n+1): #n choose 4
                    
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

#create clauses for every 7 points
def buildcase(p1,pn,above,below):
    literals=[]#add all the individual literals here to form the final clause
    #final clause will be (literal 1 OR literal 2 OR ...)
    #we want to create the clause that makes it a convex heptagon and add its negation
    #EX: If we require (literal 1 AND literal 2 AND ...) to have this configuration of a convex heptagon, we will negate to get (~literal 1 OR ~literal 2 OR ...)

    above.append(pn)#above stores (p1, ... , pn) ... is all the triples (p1,pi,pn) that are caps which means pi is above the line from p1 to pn
    below.append(pn)#below is same as above but for when (p1,pi,pn) are cups, so pi is below the line from p1 to pn


    for i in range(1,len(above)-1):#all elements in above except p1 and pn
        p_i =above[i]
        literals.append(-1*triple_vars[(p1,p_i,pn)])#if (p1,pi,pn) is a cap then add ~(p1,pi,pn)
    
    for i in range(1,len(below)-1):#all elements in below except p1 and pn
        p_i =below[i]
        literals.append(triple_vars[(p1,p_i,pn)])#if (p1,pi,pn) is a cup then add ~(p1,pi,pn)
    

    #consective triples that are above must be all caps for a convex heptagon. Same for below but with all cups.
    #EX: if points 2,3, and 5 are above and 4,6 are below and p1=1 and pn=7 then (1,2,3) and (2,3,5) and (3,5,7) must be caps and (1,4,6) and (4,6,7) must be cups.

    if (len(above) > 3):#if more than 1 point is above
        for i in range(len(above)-2):
            literals.append(-1*triple_vars[(above[i],above[i+1],above[i+2])])
    
    if (len(below) > 3):#if more than 1 point is below
        for i in range(len(below)-2):
            literals.append(triple_vars[(below[i],below[i+1],below[i+2])])
    
    above.pop()#remove pn from above
    below.pop()#remove pn from below
    return literals

def iterative(p1,p2,p3,p4,p5,p6,p7):#iterate through all possible configurations of cup or cap
    above=[p1]#above stores (p1, ... , pn) ... is all the triples (p1,pi,pn) that are caps which means pi is above the line from p1 to pn
    below=[p1]#below is same as above but for when (p1,pi,pn) are cups, so pi is below the line from p1 to pn
    
    for i2 in range(2):#triple (p1,p2,pn) 0 = cup, 1 is cap
        last2=False     #was this triple a cap on its last iteration (True) or a cup (False)
        if (i2 == 1):
            above.append(p2)#if cap then it is above the line
            last2=True
        else:
            below.append(p2)#since cup, it is below
            last2 = False
        
        for i3 in range(2):#triple (p1,p3,pn) 0 = cup, 1 is cap
            last3=False
            if (i3 == 1):
                above.append(p3)
                last3=True
            else:
                below.append(p3)
                last3 = False

            for i4 in range(2):#triple (p1,p4,pn) 0 = cup, 1 is cap
                last4=False
                if (i4 == 1):
                    above.append(p4)
                    last4=True
                else:
                    below.append(p4)
                    last4 = False
                for i5 in range(2):#triple (p1,p5,pn) 0 = cup, 1 is cap
                    last5=False
                    if(i5 == 1):
                        above.append(p5)
                        last5=True
                    else:
                        below.append(p5)
                        last5=False
                    for i6 in range(2):#triple (p1,p6,pn) 0 = cup, 1 is cap
                        last6=False
                        if(i6 == 1):
                            above.append(p6)
                            last6=True
                        else:
                            below.append(p6)
                            last6=False

                        cnf.append(buildcase(p1,p7,above,below))#add the clause built in buildcase
                        
                        #remove old entries of above/below after configuration was already built
                        if (last6): above.pop()#if this triple was last a cap (above) then remove it from above
                        else: below.pop()      #if it was last below then remove from below
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
                        for p7 in range(p6+1,n+1): #N choose 7
                            iterative(p1,p2,p3,p4,p5,p6,p7)#create configuration for given 7 points


solver = Glucose42()
solver.append_formula(cnf)

end_build = time.time()
build_time = end_build-start_build
print(f"Built variables & clauses in {build_time} seconds")

def writeCNF():#formula to write CNF File if needed
    with open("/Users/virajnain/Desktop/code/ES_Problem/output5.cnf", "w") as file:
        file.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")

start_solve=time.time()
sat=solver.solve()
end_solve=time.time()
solving_time=end_solve-start_solve
print(f"Solved in {solving_time:.4f} seconds")

def writeProof(proof):#writes UNSAT proof in DRUP format into a file
    with open("/Users/virajnain/Desktop/code/ES_Problem/proof.cnf","w") as file:
        for s in proof:
            file.write(f"{s}\n")

if (sat):
    print("SAT\n")
    #print(solver.get_model())
else:
    print("UNSAT")
    proof=solver.get_proof()#proof value is an array of strings
    writeProof(proof)