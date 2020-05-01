class MAIN:
    from NFA import NFA
    from DFA import DFA

    s = str(input("states:"))
    s = s[1:len(s)-1]
    states = s.split(',')

    s = str(input("terminals:"))
    s = s[1:len(s)-1]
    terminals = s.split(',')

    n = int(input("transitions number:"))
    transitions = []
    for i in range(0, n):
        t = str(input("transition: ")).split(",")
        if t[2] == '':
            t[2] = 'landa'
        transitions.append(t)

    s = str(input("final states:"))
    s = s[1:len(s)-1]
    finalStates = s.split(',')

    myNFA = NFA(states, terminals, transitions, finalStates)
    myDFA = DFA(states, terminals, transitions, finalStates)
    print("what do you want?")
    print("1=Is accepted by NFA")
    print("2=Find NFA regex")
    print("3=Find DFA regex")
    print("4=Create equevalent DFA")
    print("5=Is accepted by DFA")
    print("6=Make simple DFA")
    print("7=NFA shape")
    print("8=DFA shape")
    print("0=END")
    while True:
        select = input("write your choise: ")
        if select == '1':
            print(myNFA.IsAcceptByNFA(states[0], input("Is accepted by NFA: ")))
        if select=='2':
            print(myNFA.FindRegex())
        if select=='3':
            print(myDFA.FindRegex())
        # if select=='4':
        if select == '5':
            print(myDFA.IsAcceptByDFA(states[0], input("Is accepted by DFA: ")))
        if select=='6':
            newDFA = myDFA.MakeSimpleDFA()
        # if select=='7':
        # if select=='8':
        if select == '0':
            break

