class MAIN:
    from NFA import NFA
    from DFA import DFA
    
    s = str(input("states:"))
    s = s[1:len(s)-1]
    states = s.split(',')

    s = str(input("terminals:"))
    s = s[1:len(s)-1]
    terminals = s.split(',')

    class transition:
        def __init__(self, start, end, terminal):
            self.start = start
            self.end = end
            self.terminal = terminal
    n = int(input("transitions number:"))
    transitions = []
    for i in range(0, n):
        t = str(input("transition: ")).split(",")
        if t[2] == '':
            t[2]='landa'
        print(t)
        transitions.append(transition(t[0], t[1], t[2]))

    s = str(input("final states:"))
    s = s[1:len(s)-1]
    finalStates = s.split(',')

    myNFA=NFA(states,terminals,transitions,finalStates)
    myDFA=DFA(states,terminals,transitions,finalStates)

