import numpy as np
from automata.fa.nfa import NFA
import copy
import itertools
from copy import deepcopy 
from queue import Queue, PriorityQueue

def initSignature(grid):
    classes=['key','door','nail']
    G=np.asarray(grid)
    unique, counts = np.unique(G, return_counts=True)
    freq=dict(zip(unique, counts))
    numberOfObjects=[freq['K'],freq['D'],freq['N']]
    objects={}
    for i,c in enumerate(classes):
        for n in range(numberOfObjects[i]):
            objects[c+str(n)]=c
    predicates=['at']
    arity={'at':1}

    return {'predicates':predicates,'objects':objects,'arity':arity}

def updateObjects(signature,addlist,dellist):
    #addlist should be a list of tuples (object_name,class)
    for item in addlist:
        signature['objects'][item[0]]=item[1]
    #dellist should be a list of names
    for name in dellist:
        try:
            del signature['objects'][name]
        except:
            pass

def literalSet(signature):
    literals=[]
    for p in signature['predicates']:
        for objs in list(itertools.combinations(list(signature['objects']),signature['arity'][p])):
            ground_literal=p+str(objs)
            ground_literal=ground_literal.replace("'","")
            ground_literal=ground_literal.replace(",)",")")            
            literals.append({'formula':ground_literal, 'predicate':p, 'neg':False, 'args':objs, 'classes':[signature['objects'][arg] for arg in objs]})
            literals.append({'formula':'not('+ground_literal+')', 'predicate':p, 'neg':True, 'args':objs, 'classes':[signature['objects'][arg] for arg in objs]})
    return literals
            
#'state' is a dictionary with the position of every existing object
def truthAssignment(State,signature):
    assignment=[]
    for p in signature['predicates']:
        for objs in list(itertools.combinations(list(signature['objects']),signature['arity'][p])):
            ground_literal=p+str(objs)
            ground_literal=ground_literal.replace("'","")
            ground_literal=ground_literal.replace(",)",")")            
            if p=='at':
                if State['robot']==State[objs[0]]:
                    assignment.append({'formula':ground_literal, 'predicate':p, 'neg':False, 'args':objs, 'classes':[signature['objects'][arg] for arg in objs]})
                else:
                    assignment.append({'formula':'not('+ground_literal+')', 'predicate':p, 'neg':True, 'args':objs, 'classes':[signature['objects'][arg] for arg in objs]})
            #add sections for other predicates (if needed) with elif
    return assignment

#this is very specific to the predefined advices
def evalulateEdge(assignment,edge):
    if (edge=='at(key0)')|(edge=='at(door0)'):
        formulae=[item['formula'] for item in assignment]
        return edge in formulae
    elif edge=='all(nail,not(at(nail)))':
        truth=[]
        for a in assignment:
            if (a['predicate']=='at')&(a['classes'][0]=='nail'):
                truth.append(a['neg'])
        return all(truth)

#creates NFA for predefined advices
def initNFA(userAdvice):
    #userAdvice is a list with the indeces of the predefined advices given by the user throught the GUI
    automataNFA=[]
    inputUpdateNFA=[]
    sym2edge=[]
    char_index=0
    #eventually(and(at(key0),next(eventually(at(door0)))))
    '''digraph automaton_for_ltl { 
    rankdir=LR;
    size="6,3" 
    node [shape = doublecircle];s_1 ;
    node [shape = circle];
    s_2 -> s_2 [ label = "[]" ];
    s_2 -> s_3 [ label = "[at(key)]" ];
    s_3 -> s_3 [ label = "[]" ];
    s_3 -> s_1 [ label = "[at(door)]" ];
    s_1 -> s_1 [ label = "[]" ];
    }'''
    edges=['at(key0)','at(door0)']
    edges_to_symbols={}
    symbols_to_edges={}
    for edge in edges:
        edges_to_symbols[edge]=chr(char_index)
        symbols_to_edges[chr(char_index)]=edge
        char_index+=1
    advice = NFA(
        states={'q0', 'q1', 'q2'},
        input_symbols=set(list(symbols_to_edges)),
        transitions={
            'q0': {edges_to_symbols['at(key0)']: {'q0','q1'}, edges_to_symbols['at(door0)']: {'q0'}},
            'q1': {edges_to_symbols['at(key0)']: {'q1'}, edges_to_symbols['at(door0)']: {'q1','q2'}},
            'q2': {edges_to_symbols['at(key0)']: {'q2'}, edges_to_symbols['at(door0)']: {'q2'}}
        },
        initial_state='q0',
        final_states={'q2'}
    )
    automataNFA.append(advice)
    inputUpdateNFA.append(createAddFunc(edges_to_symbols))
    sym2edge.append(symbols_to_edges)
    '''digraph automaton_for_ltl { 
    rankdir=LR;
    size="6,3" 
    node [shape = doublecircle];s_1 ;
    node [shape = circle];
    s_2 -> s_2 [ label = "[all(nail,not(at(nail)))]" ];
    s_2 -> s_1 [ label = "[all(nail,not(at(nail)))]" ];
    }'''
    edges=['all(nail,not(at(nail)))']
    edges_to_symbols={}
    symbols_to_edges={}
    for edge in edges:
        edges_to_symbols[edge]=chr(char_index)
        symbols_to_edges[chr(char_index)]=edge
        char_index+=1
    advice = NFA(
        states={'q0', 'q1'},
        input_symbols=set(list(symbols_to_edges)),
        transitions={
            'q0': {edges_to_symbols['all(nail,not(at(nail)))']: {'q0','q1'}},
            'q1': {}
        },
        initial_state='q0',
        final_states={'q1'}
    )
    automataNFA.append(advice)
    inputUpdateNFA.append(createAddFunc(edges_to_symbols))
    sym2edge.append(symbols_to_edges)

    automataNFA=[a for i,a in enumerate(automataNFA) if i in userAdvice]
    inputUpdateNFA=[f for i,f in enumerate(inputUpdateNFA) if i in userAdvice]
    sym2edge=[s for i,s in enumerate(sym2edge) if i in userAdvice]    
    return (automataNFA,inputUpdateNFA,sym2edge)
    
def createAddFunc(edges_to_symbols):
    def addSymbols(assignment,seq):
        for edge in list(edges_to_symbols):
            if evalulateEdge(assignment,edge):
                seq+=edges_to_symbols[edge]
        return seq
    return addSymbols

def usefulEdges(initialStates,acceptingStates,transitionFunction,sym2edge):
    usefulEdges=set()
    for si in initialStates:
        possEdges=list(transitionFunction[si])
        nextStates={}
        for edge in possEdges:
            for state in transitionFunction[si][edge]:
                if state in nextStates:
                    nextStates[state].add(sym2edge[edge])
                else:
                    nextStates[state]=set([sym2edge[edge]])           
        for sn,edges in nextStates.items():
            if sn!=si:
                if conditionedReachability(sn,acceptingStates,si,transitionFunction):
                    usefulEdges|=edges
    return usefulEdges

def conditionedReachability(initialState,acceptingStates,forbiddenState,transitionFunction):
    previousReachSet=set()
    currentReachSet={initialState}
    while (currentReachSet-previousReachSet):
        previousReachSet=copy.deepcopy(currentReachSet)
        oneStepReachableStates=set()
        for state in previousReachSet:
            for edge in list(transitionFunction[state]):
                oneStepReachableStates|=transitionFunction[state][edge]
        currentReachSet|=(oneStepReachableStates-{forbiddenState})
    return bool(currentReachSet & acceptingStates)

def runNFA(automataNFA,inputUpdateNFA,sym2edge,inputSequences,currentStates,tA):
    useful=[]
    for i,f in enumerate(inputUpdateNFA):
        emptySet=False
        seq=f(tA,inputSequences[i])
        state_generator = automataNFA[i].read_input_stepwise(seq)
        try:
            for config in state_generator:
                if config:
                    currentStates[i]=config
                else:
                    emptySet=True
                    break
        except:
            pass
        if not emptySet:
            inputSequences[i]=seq
        useful.append(list(usefulEdges(currentStates[i],automataNFA[i].final_states,automataNFA[i].transitions,sym2edge[i])))
    return useful

def hB(State,Action,literal,litSet):
    highValue=1000
    formulae=[lit['formula'] for lit in litSet]
    try:
        parsedLit=litSet[formulae.index(literal)]
        if parsedLit['predicate']=='at':
            robotPos=State['robot']
            itemPos=State[parsedLit['args'][0]]
            diff=[r-i for r,i in zip(robotPos,itemPos)]
            sign_diff=np.sign(diff)
            delta=0
            if sign_diff[1]==1:
                deltaAdd={'R':1,'L':-1,'U':0,'D':0}
                delta+=deltaAdd[Action]
            elif sign_diff[1]==0:
                deltaAdd={'R':1,'L':1,'U':0,'D':0}
                delta+=deltaAdd[Action]
            elif sign_diff[1]==-1:
                deltaAdd={'R':-1,'L':1,'U':0,'D':0}
                delta+=deltaAdd[Action]
            if sign_diff[0]==1:
                deltaAdd={'R':0,'L':0,'U':-1,'D':1}
                delta+=deltaAdd[Action]
            elif sign_diff[0]==0:
                deltaAdd={'R':0,'L':0,'U':1,'D':1}
                delta+=deltaAdd[Action]
            elif sign_diff[0]==-1:
                deltaAdd={'R':0,'L':0,'U':1,'D':-1}
                delta+=deltaAdd[Action]
            heuristic=np.sum(np.abs(diff))+delta
            if parsedLit['neg']:
                if heuristic==0:
                    heuristic=1
                else:
                    heuristic=0
    except ValueError:
        heuristic=highValue
    return heuristic

def hFunction(advice,State,Aset,litSet,mode):
    if mode=='guidance':
        heuristics={a:1000 for a in Aset}
        for a in Aset:
            for nfa in advice:
                hNFA=1000
                for formula in nfa:
                    if formula=='all(nail,not(at(nail)))':
                        hFO=-1000
                        for lit in litSet:
                            if 'not(at(nail' in lit['formula']:
                                hFO=max(hFO,hB(State,a,lit['formula'],litSet))
                        hNFA=min(hNFA,hFO)
                    else:
                        hNFA=min(hNFA,hB(State,a,formula,litSet))
                heuristics[a]=min(heuristics[a],hNFA)
    elif mode=='warning':
        heuristics={a:-1000 for a in Aset}
        for a in Aset:
            for nfa in advice:
                hNFA=1000
                for formula in nfa:
                    if formula=='all(nail,not(at(nail)))':
                        hFO=-1000
                        for lit in litSet:
                            if 'not(at(nail' in lit['formula']:
                                hFO=max(hFO,hB(State,a,lit['formula'],litSet))
                        hNFA=min(hNFA,hFO)
                    else:
                        hNFA=min(hNFA,hB(State,a,formula,litSet))
                heuristics[a]=max(heuristics[a],hNFA)
    return heuristics


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
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                return [i, j, 0]
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
    end = False
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
    if is_terminal_state(grid, s_prime):
         end = True
    return s_prime, r, end

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
        s_prime, _, _ = execute_action(grid, s, a)
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
        s_prime, _, _ = execute_action(grid, s, best_action)
        s = s_prime
        if cc==40:
            break
        
    return plan

def get_state_dict(grid, S, signature):
    addlist=[]
    dellist=[]
    G=np.asarray(grid)
    State={}
    nails=0
    State['robot']=S[0:2]
    for o,c in signature['objects'].items():
        if o=='key0':
            find=np.where(G=='K')
            keyState=[find[0][0],find[1][0]]
            if S[2]==0:                
                State[o]=keyState
            elif keyState==S[0:2]: #assuming the grid is not updated when the robot takes the key
                State[o]=keyState
            else:
                dellist.append('key0')
        elif o=='door0':
            find=np.where(G=='D')
            State[o]=[find[0][0],find[1][0]]
        elif c=='nail':
            find=np.where(G=='N')
            State[o]=[find[0][nails],find[1][nails]]
            nails+=1
    return State,addlist,dellist

def Rmax(grid, S, A, N, sig, setNFA):
    T_unknown = init_T(grid, S, A)
#    print("T_unknown: ", len(T_unknown))
    P_hat = []
    s = get_initial_state(grid)
    t = 0
    policy = []
    cap = 0
    capacity=0
    learning = []
    automataNFA,inputUpdateNFA,sym2edge=setNFA
    signature=copy.deepcopy(sig)
    inputSequences=['']*len(automataNFA)
    currentStates=[nfa.initial_state for nfa in automataNFA]
    while t < N and len(T_unknown):
        t += 1
        State,addlist,dellist=get_state_dict(grid,s,signature)
        updateObjects(signature,addlist,dellist)
        litSet=literalSet(signature)
        tA=truthAssignment(State,signature)
        useful=runNFA(automataNFA,inputUpdateNFA,sym2edge,inputSequences,currentStates,tA)
        heuristics=hFunction(useful,State,A,litSet,mode='guidance')
        #heuristics gives a dictionary, where a heuristic value for each action given the current state
        #for example {'U': 10, 'D': 12, 'R': 12, 'L': 10}, Less is better
#        print ("S: ", s)
        mn = float("INF")
        mn_action = ""
        unknown = 0
        for a in heuristics:
            if valid(grid, s, a) and ([s, a] in T_unknown):
                unknown = 1
                if heuristics[a] < mn:
                    mn = heuristics[a]
                    mn_action = a
        
        if unknown == 1:
            s_prime, r, end = execute_action(grid, s, mn_action)
            learning.append(mn_action)
            P_hat.append([s, mn_action, s_prime, r])
            T_unknown.remove([s, mn_action])

            
        if unknown == 0:
            index = find(s, policy)
            if index == -1 or (cap==capacity and cap):
                policy = get_policy_BFS(grid, s, A, P_hat, T_unknown)
                cap = 0
                capacity = len(policy)
                index = find(s, policy)
            cap += 1            
            a = policy[index][1]
            learning.append(a)
            s_prime, r, end = execute_action(grid, s, a)
            if [s, a] in T_unknown:
                P_hat.append([s, a, s_prime, r])
                T_unknown.remove([s, a])

        s = s_prime
        
                
        if is_terminal_state(grid, s):
            s = get_initial_state(grid)
        
        if end:
            signature=copy.deepcopy(sig)
            inputSequences=['']*len(automataNFA)
            currentStates=[nfa.initial_state for nfa in automataNFA]

    return learning, compute_optimal_plan(P_hat, grid)

 
"""""
DEBUGGING
"""""

def main(grid, advice):
    N = 600
    A = ['U', 'D', 'R', 'L']
    h = len(grid)
    w = len(grid[0])
    S = init_S(grid, h, w)
    signature=initSignature(grid)
    setNFA=initNFA(userAdvice=advice)
    return Rmax(grid, S, A, N, signature, setNFA)
 
