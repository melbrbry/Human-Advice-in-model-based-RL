"""
Created on Fri May  4 02:07:20 2018

@author: elbarbari
"""
from queue import Queue
from copy import deepcopy 

def valid(grid, s, a):
    row = s[0]
    col = s[1]
    key = s[2]
    height = len(grid)
    width = len(grid[0])
    if is_terminal_state(grid, s):
        return False
    if a == 'U':
        if row-1<0 or grid[row-1][col] == '*' or (grid[row-1][col]=='D' and not key):
            return False
        else:
            return True
    if a == 'D':
        if row+1==height or grid[row+1][col] == '*' or (grid[row+1][col]=='D' and not key):
            return False
        else:
            return True
    if a == 'R':
        if col+1==width or grid[row][col+1] == '*' or (grid[row][col+1]=='D' and not key):
            return False
        else:
            return True
    if a == 'L':
        if col-1<0 or grid[row][col-1] == '*' or (grid[row][col-1]=='D' and not key):
            return False
        else:
            return True
        
    return True

def get_initial_state(grid):
    for i in range(len(grid)):
        for ii in range(len(grid[0])):
            if grid[i][ii]=='S':
                return [i, ii, 0]
    print("no Subject in grid, default [5,12]")
    return [5, 12, 0]

def is_terminal_state(grid, s):
    row = s[0]
    col = s[1]
    key = s[2]
    if grid[row][col]=='D' and key:
        return True
    return False

def init_S(grid, h, w):
    S = []
    for i in range(h):
        for j in range(w):
            if grid[i][j] not in ['*']:
                if not grid[i][j] in ['K', 'D']:
                    S.append([i,j,0])
                S.append([i,j,1])
    return S     

def init_T(grid, S, A):
    T = []
    for s in S:
        for a in A:
            if valid(grid, s, a):
                T.append([s, a])
    return T

def execute_action(grid, s, a):
    row = s[0]
    col = s[1]
    key = s[2]
    r = -1
    if a == 'U':
        row -= 1
    if a == 'D':
        row += 1
    if a == 'R':
        col += 1
    if a == 'L':
        col -= 1
    if grid[row][col]=='N':
        r -= 10
    if grid[row][col]=='D':
        r += 1000
    if grid[row][col]=='K':
        key = 1
    s_prime = [row, col, key]
#    if learning and is_terminal_state(grid, s_prime):
#        s_prime = get_initial_state()
    return s_prime, r

def reward(grid, s):
    row = s[0]
    col = s[1]
    r = -1
    if grid[row][col]=='N':
        r -= 10
    if grid[row][col]=='D':
        r += 1000
    return r


def get_path(t, parents, s0):
#    print (parents)
    path = [t]
    exist = True
    while exist:
        exist = False
        for relation in parents:
            child = relation[0]
            parent = relation[1]
#            print (child, " <--", parent)
            if child == t:
                path.append(parent)
                if parent[0]==s0:
                    return path
                exist = True
                t = parent
                break
    return path
    
def get_policy_BFS(grid, s, A, P_hat, T_unknown):
    s0 = s
    q = Queue()
    parents = []
    visited = []
    for a in A:
        if valid(grid, s, a):
            q.put([s, a])
            visited.append([s, a])
    while not q.empty():
        t = q.get()
        if t in T_unknown:
            return get_path(t, parents, s0)
        s = t[0]
        a = t[1]
        s_prime, _ = execute_action(grid, s, a)
        s = s_prime
        if is_terminal_state(grid, s):
            s = get_initial_state(grid)
        for a in A:
            if valid(grid, s, a) and [s, a] not in visited:
                q.put([s, a])
                parents.append([[s, a], t])
                visited.append([s, a])
    return -1
        
def find(s, policy):
    for i in range(len(policy)):
        if s==policy[i][0]:
            return i
    return -1

def value_iteration(grid, S, P_hat):
    gamma = 1
    max_iter = 50
    V_old = []
    for s in S:
        V_old.append([s,0])
    V_new = deepcopy(V_old)
    
    for i in range(max_iter):
#        print("iteration: ", i)
        for i in range(len(V_new)):
            s = V_new[i][0]
#            print("s:", s)
            if is_terminal_state(grid, s):
                V_new[i][1] = reward(grid, s)
                continue
            mx = -float("INF")
            for it in P_hat:
                if it[0]==s:
                    value = reward(grid, s)
                    s_prime = it[2]
          #          print("s_prime: ", s_prime)
                    for v in V_old:
                        if v[0]==s_prime:
                            value += gamma * v[1]
                            break
                    mx = max(mx, value)
            V_new[i][1] = mx
        V_old = deepcopy(V_new) 
#        print("xxxxxxxxxxxxxxxxxxxx")
#        for it in V_old:
#            print(it)
    return V_old
                    

def compute_optimal_plan(P_hat, grid):
    S = []
    for it in P_hat:
        if not it[0] in S:
            S.append(it[0])
        if not it[2] in S:
            S.append(it[2])
   # print ("len of S known: ", len(S))
    V = value_iteration(grid, S, P_hat)
#    for v in V:
#        print (v)
#    print("Value Iteration DONE!")
    s = get_initial_state(grid)
    plan = []
    cc = 0
    while not is_terminal_state(grid, s):
        cc += 1
        mx = -float("INF")
#        print ("s:", s)
        best_action = ""
        for it in P_hat:
            if it[0]==s:
                s_prime = it[2]
#                print ("", it[1])
                for v in V:
                    if v[0]==s_prime:
                        value = v[1]
#                print ("value: ", value)
                if value > mx:
                    mx = value 
                    best_action = it[1]
#        print("best action: ", best_action)
        plan.append(best_action)
        s_prime, _ = execute_action(grid, s, best_action)
        s = s_prime
        if cc==40:
            break
        
    return plan
        
def Rmax(grid, S, A, N):
    T_unknown = init_T(grid, S, A)
#    print("T_unknown: ", len(T_unknown))
    P_hat = []
    s = get_initial_state(grid)
    t = 0
    policy = []
    cap = 0
    capacity=0
    learning = []
    while t < N and len(T_unknown):
        if is_terminal_state(grid, s):
#            print("yes ", t)
            s = get_initial_state(grid)
        t += 1
#        print ("step: ", t)            
        index = find(s, policy)
        if index == -1 or (cap==capacity and cap):
            policy = get_policy_BFS(grid, s, A, P_hat, T_unknown)
            cap = 0
            capacity = len(policy)
            index = find(s, policy)
        cap += 1
#        print ("index: ", index)
#        print ("policy: ", policy)
        
        a = policy[index][1]
        learning.append(a)
#        print ("action: ", a)
        s_prime, r = execute_action(grid, s, a)
#        print ("s_prime: ", s_prime)
        if [s, a] in T_unknown:
            P_hat.append([s, a, s_prime, r])
            T_unknown.remove([s, a])
        s = s_prime
#        print (len(T_unknown))
#    print("T_unknown: ", len(T_unknown))
#    print("steps: ", t)
#    print("T_unknown: ", T_unknown)
#    print("Len of P_hat: ", len(P_hat))
#    for it in P_hat:
#        print(it)
    return learning, compute_optimal_plan(P_hat, grid)




def main(grid):
    N = 1000
    A = ['U', 'D', 'R', 'L']
    h = len(grid)
    w = len(grid[0])
    S = init_S(grid, h, w)
    return Rmax(grid, S, A, N)
    


"""""
DEBUGGING
#"""""

#grid = [['*', '*', '*', '*','*','*','*','*','*','*','*','*','*','*'],
#        ['*','.', '.', '.', 'N','N','N','N','N','N','.','.','.','*'],
#        ['.','.', '.', '.', 'N','N','N','N','N','N','.','.','.','*'],
#        ['*','.', '.', '.', 'N','N','N','N','N','N','.','.','.','*'],
#        ['*','.', 'K', '.', '.','.','.','.','D','.','.','.','.','*'],
#        ['*','.', '.', '.', '.','.','.','.','.','.','.','.','.','*'],
#        ['*', '*', '*', '*','*','*','*','*','*','*','*','*','*','*']]


#grid = [['*', '*', '*', '*','*','*','*','*','*','*','*','*','*','*'],
#        ['*','.', '.', '.', 'N','K','N','N','N','N','.','.','.','*'],
#        ['.','.', '.', '.', 'N','N','N','N','N','N','.','.','.','*'],
#        ['*','.', '.', '.', 'N','N','N','N','N','N','.','.','.','*'],
#        ['*','.', '.', '.', '.','.','.','.','D','.','.','.','.','*'],
#        ['*','.', '.', '.', '.','.','.','.','.','.','.','.','.','*'],
#        ['*', '*', '*', '*','*','*','*','*','*','*','*','*','*','*']]


        
def init_S_debug():
    print (init_S(grid, h, w))

#init_S_debug()
    
def init_T_debug():
    S = init_S(grid, h, w)
    print (init_T(grid, S, A))
    
#init_T_debug()

def is_terminal_state_debug():
    print (is_terminal_state(grid, [1, 13, 1]))
    print (is_terminal_state(grid, [1, 13, 0]))
    print (is_terminal_state(grid, [2, 13, 1]))
    
#is_terminal_state_debug()

def valid_debug():
    print (valid(grid, [1, 12, 0], 'R'))
    print (valid(grid, [1, 12, 1], 'R'))

#valid_debug()
