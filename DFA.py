import copy
class DFA:
    def __init__(self, states, terminals, transitions, finalStates):
        self.states = states
        self.terminals = terminals
        self.transitions = transitions
        self.finalStates = finalStates
        self.regex = ''
        self.ds = {}
        self.transition_dict = {}
        self.set_transition_dict()

    def IsAcceptByDFA(self, firstState, s):
        result = False
        if(len(s) == 0):
            if(firstState in self.finalStates):
                return True
            else:
                return False
        else:
            for t in self.transitions:
                if t[0] == firstState and t[2] == s[0] and result == False:
                    result = self.IsAcceptByDFA(t[1], s[1:len(s)])
            return result
        return result

    def FindRegex(self):
        print('Define the transition function : ')
        transition_matrix = [list(map(str, input().split())) for _ in range(len(self.states))]
        transitions = dict(zip(self.states, transition_matrix))
        r = ''
        for f in self.finalStates:
            dfa = DFA(self.states, self.terminals,transitions,[f])
            r+= '+' + dfa.toregex()
        return(r[1:])

    def MakeSimpleDFA(self):
        again=True
        g={}
        n=1
        for st in self.states:
            if(not st in self.finalStates):
                g[st]='g0'    
            else:
                g[st]='g'+str(n)
        while again==True:
            again=False
            newTransitions=[]
            for t in self.transitions:
                t1=[g[t[0]],g[t[1]],t[2]]
                newTransitions.append(t1)
            for i in range(0,len(newTransitions)):
                for j in range(i+1,len(newTransitions)):
                    transition1=newTransitions[i]
                    transition2=newTransitions[j]
                    if transition1[0]==transition2[0] and transition1[2]==transition2[2] and transition1[1]!=transition2[1]:
                        n=n+1
                        again=True
                        t2=self.transitions[j]
                        changeIndex=t2[0]
                        g[changeIndex]='g'+str(n)
                        break
                if(again==True):
                    break
        newStates=[]
        newFinals=[]
        for state in self.states:
            if not g[state] in newStates:
                newStates.append(g[state])
            if (state in self.finalStates) and (not g[state] in newFinals):
                newFinals.append(g[state])
        for i in range(0,len(newTransitions)):
                for j in range(i+1,len(newTransitions)):
                    transition1=newTransitions[i]
                    transition2=newTransitions[j]
                    if transition1[0]==transition2[0] and transition1[2]==transition2[2] and transition1[1]==transition2[1]:
                        newTransitions[i]=[['arman','mostafa','heydari']]
        newNewTransitions=[]
        for t in newTransitions:
            if(t!=[['arman','mostafa','heydari']]):
                newNewTransitions.append(t)
        newDFA=DFA(newStates,self.terminals,newNewTransitions,newFinals)
        return newDFA

    def Shape(self):
        pass

    def set_transition_dict(self):
        dict_states = {r: {c: 'ϕ' for c in self.states} for r in self.states}
        for i in self.states:
            for j in self.states:
                indices = [ii for ii, v in enumerate(self.transitions[i]) if v == j]
                if len(indices) != 0:
                    dict_states[i][j] = '+'.join([str(self.terminals[v]) for v in indices])
        self.ds = dict_states
        self.transition_dict = copy.deepcopy(dict_states)
    
    def get_intermediate_states(self):
        return [state for state in self.states if state not in ([self.states[0]] + self.finalStates)]

    def get_predecessors(self, state):
        return [key for key, value in self.ds.items() if state in value.keys() and value[state] != 'ϕ' and key != state]

    def get_successors(self, state):
        return [key for key, value in self.ds[state].items() if value != 'ϕ' and key != state]

    def get_if_loop(self, state):
        if self.ds[state][state] != 'ϕ':
            return self.ds[state][state]
        else:
            return ''

    def toregex(self):
        intermediate_states = self.get_intermediate_states()
        dict_states = self.ds

        for inter in intermediate_states:
            predecessors = self.get_predecessors(inter)
            successors = self.get_successors(inter)
            for i in predecessors:
                for j in successors:
                    inter_loop = self.get_if_loop(inter)
                    dict_states[i][j] = '+'.join(('(' + dict_states[i][j] + ')', ''.join(('(' + dict_states[i][
                        inter] + ')', '(' + inter_loop + ')' + '*', '(' + dict_states[inter][j] + ')'))))

            dict_states = {r: {c: v for c, v in val.items() if c != inter} for r, val in dict_states.items() if
                           r != inter}
            self.ds = copy.deepcopy(dict_states)

        init_loop = dict_states[self.states[0]][self.states[0]]
        init_to_final = dict_states[self.states[0]][self.finalStates[0]] + '(' + dict_states[self.finalStates[0]][
            self.finalStates[0]] + ')' + '*'
        final_to_init = dict_states[self.finalStates[0]][self.states[0]]
        re = '(' + '(' + init_loop + ')' + '+' + '(' + init_to_final + ')' + '(' + final_to_init + ')' + ')' + '*' + '(' + init_to_final + ')'
        return re
