# Improve strategy: Use all 52 rows with backtracking but with pruning: maintain echelon as we go through rows in fixed order.
import re,ast
from Crypto.Util.number import long_to_bytes
import numpy as np

text=open('dist/out.txt').read()
A_list=ast.literal_eval(re.search(r'A_values\s*=\s*(\[.*?\])\s*;\s*b_values\s*=\s*(\[.*\])\s*$', text, re.S).group(1))
b_list=ast.literal_eval(re.search(r'A_values\s*=\s*(\[.*?\])\s*;\s*b_values\s*=\s*(\[.*\])\s*$', text, re.S).group(2))
p=0x225fd
E=[97491%p,14061%p,55776%p]
A=np.array(A_list, dtype=int)%p
b=np.array(b_list, dtype=int)%p
n, m = A.shape
p=int(p)

def modinv(a):
    a=int(a)%p
    if a==0:
        return None
    return pow(a, p-2, p)

bestS=None
found=False

# We'll build an augmented matrix with dynamic rows up to rank m; stop when rank reaches m and solve, but still must be consistent with remaining rows.

# State: current echelon matrix Mech (reduced on-the-fly), rhs vector, and a mapping from pivot columns.

Mech=np.zeros((0,m), dtype=object)
rhs=np.zeros((0,), dtype=object)

order=list(range(n))

solS=None

def add_equation(Me, rh, rowA, val):
    # Add Arow · x = val, reduce with current echelon
    row=rowA.copy().astype(object)
    v=int(val)%p
    # eliminate using existing pivots
    # find pivots
    pivots=[]
    for i in range(Me.shape[0]):
        # find pivot col
        pc=None
        for c in range(m):
            if int(Me[i,c])%p!=0:
                pc=c; break
        pivots.append(pc)
        if pc is not None:
            factor=int(row[pc])%p
            if factor!=0:
                row=(row - factor*Me[i])%p
                v=(v - factor*rh[i])%p
    # now check if row is zero
    if all(int(row[c])%p==0 for c in range(m)):
        if v%p!=0:
            return None, None, False  # inconsistent
        else:
            return Me, rh, True  # redundant
    # find new pivot
    pc=None
    for c in range(m):
        if int(row[c])%p!=0:
            pc=c; break
    inv=modinv(row[pc])
    if inv is None:
        return None, None, False
    row=(row*inv)%p
    v=(v*inv)%p
    # eliminate this pivot from above rows to keep RREF-ish
    if Me.shape[0]>0:
        Me2=Me.copy(); rh2=rh.copy()
        for i in range(Me.shape[0]):
            factor=int(Me2[i,pc])%p
            if factor!=0:
                Me2[i]=(Me2[i] - factor*row)%p
                rh2[i]=(rh2[i] - factor*v)%p
        # append
        Me2=np.vstack([Me2, row])
        rh2=np.concatenate([rh2, np.array([v], dtype=object)])
        return Me2, rh2, True
    else:
        Me2=np.vstack([row])
        rh2=np.array([v], dtype=object)
        return Me2, rh2, True


def extract_solution(Me, rh):
    x=[0]*m
    # rows assumed in RREF-ish form with pivot 1 and zeros elsewhere
    # get pivot columns
    pivots=[]
    for i in range(Me.shape[0]):
        pc=None
        for c in range(m):
            if int(Me[i,c])%p!=0:
                pc=c; break
        pivots.append(pc)
    for i in range(Me.shape[0]-1, -1, -1):
        pc=pivots[i]
        if pc is None:
            continue
        s=rh[i]
        for c in range(pc+1, m):
            if int(Me[i,c])%p!=0:
                s=(s - int(Me[i,c])*x[c])%p
        x[pc]=int(s)%p
    return x

best_cnt=-1
best_sol=None

# Backtracking through rows choosing e

def dfs(idx, Me, rh):
    global best_cnt, best_sol
    if idx==n or Me.shape[0]==m:
        # We have a full-rank or exhausted all rows, get candidate solution
        x=extract_solution(Me, rh)
        # count compatibility on all rows
        cnt=0
        for i in range(n):
            resid=(int(b[i]) - sum((int(A[i,j])*x[j])%p for j in range(m))%p)%p
            if resid in E:
                cnt+=1
        if cnt>best_cnt:
            best_cnt=cnt; best_sol=x
        return
    rowA=A[idx].astype(object)
    for e in E:
        val=(int(b[idx]) - e)%p
        Me2, rh2, ok = add_equation(Me, rh, rowA, val)
        if not ok:
            continue
        dfs(idx+1, Me2, rh2)

# Start
dfs(0, Mech, rhs)

print('best_cnt', best_cnt)
if best_sol:
    flag=0
    for i,si in enumerate(best_sol):
        flag += int(si)*(p**i)
    try:
        print(long_to_bytes(flag))
    except Exception as ex:
        print('decode error', ex)
        print(flag)
