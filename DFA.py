class DFA:
    def __init__(self, states, terminals, transitions, finalStates):
        self.states = states
        self.terminals = terminals
        self.transitions = transitions
        self.finalStates = finalStates

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
        result=""
        return result

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
