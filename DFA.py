class DFA:
    def __init__(self, states, terminals, transitions, finalStates):
        self.states = states
        self.terminals = terminals
        self.transitions = transitions
        self.finalStates = finalStates

    def IsAcceptedByDFA(self, firstState, s):
        result = False
        if(len(s) == 0):
            if(firstState in self.finalStates):
                return True
            else:
                return False
        else:
            for t in self.transitions:
                if t[0] == firstState and t[2] == s[0] and result == False:
                    result = self.IsAcceptedByDFA(t[1], s[1:len(s)])
            return result
        return result

    def FindRegex(self):
        pass

    def MakeSimpleDFA(self):
        pass

    def Schematic(self):
        pass
