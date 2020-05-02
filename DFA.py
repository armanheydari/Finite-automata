import copy
import pygame
import pygame.gfxdraw
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
        transition_matrix = self.transitions
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
        dfa = {}
        for i in range(len(self.states)):
            state = self.states[i]
            dfa[state] = {}
            for terminal in self.terminals:
                dfa[state][terminal] = []
                for j in range(len(self.transitions)):
                    if self.transitions[j][0] == state and self.transitions[j][2] == terminal:
                        dfa[state][terminal].append(self.transitions[j][1])
        
        for key in dfa.keys():
                for path in self.terminals:
                    if dfa[key][path] == []:
                        del dfa[key][path]
            

        pygame.init()
        BLACK = (  0,   0,   0)
        WHITE = (255, 255, 255)
        BLUE =  (  0,   0, 255)
        GREEN = (  0, 255,   0)
        RED =   (255,   0,   0)
        size = [1400, 1000]
        screen = pygame.display.set_mode(size)
        
        pygame.display.set_caption("Example code for the draw module")
        
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()
        pygame.font.init()
        while not done:
            clock.tick(10)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=True
            screen.fill(WHITE)
            i = 0
            trasition_num = len(self.transitions)
            r = 25
            distance = int(1400 / (len(self.states)+1))
            for key in dfa.keys():
                pygame.draw.circle(screen, RED, [(distance*(int(key[1:])+1)), 250], r, 0)
                pygame.draw.circle(screen, BLUE, [(distance*(int(key[1:])+1)), 250], r-4, 0)
                font = pygame.font.SysFont(None, r+2)
                text = font.render((key), True, BLACK)
                screen.blit(text, [(distance*(int(key[1:])+1))-10, 240])
            
            pi = 3.14
            i = 0  
            for st in dfa.keys():
                same_path = []
                if st in self.finalStates:
                    pygame.draw.arc(screen,BLUE,[distance*(i+1)-27, 223, r*2+4, r*2+4], -3.3, 3, 4)
                i += 1
                
                for path in dfa[st].keys():
                    w = 0
                    rs = 0
                    for reachable_state in dfa[st][path]:
                        from_state = st
                        to_state = reachable_state
                        diff = int(from_state[1:]) - int(to_state[1:])
                        abs_diff = abs(diff)
                        h = abs_diff * 100
                        font = pygame.font.SysFont(None, r+2)
                        if len(same_path) != 0 and dfa[st][same_path[0]] == dfa[st][path]:
                            text = font.render(',' + path, True, BLACK)
                            w += 1
                        else:
                            text = font.render(path, True, BLACK)
                            same_path.append(path)
                            w = 0
                        if abs_diff == 0:
                            pygame.draw.arc(screen,BLACK,[distance*(int(from_state[1:])+1), 262, 40, 40], -3.3, 1.5, 2)
                            pygame.draw.polygon(screen, BLACK, [[distance*(int(from_state[1:])+1)+20, 310],
                                                                [distance*(int(from_state[1:])+1)+20, 290],
                                                                [distance*(int(from_state[1:])+1)+12, 300]], 4)
                            screen.blit(text, [distance*(int(to_state[1:])+1)+20+(w*10), 315])
                        else:
                            if diff > 0:
                                pygame.draw.polygon(screen, BLACK, [[distance*(int(to_state[1:])+1) + distance*abs_diff/2, 235-(h/2)],
                                                                    [distance*(int(to_state[1:])+1) + distance*abs_diff/2, 215-(h/2)],
                                                                    [distance*(int(to_state[1:])+1)-8 + distance*abs_diff/2, 225-(h/2)]], 4)
                                pygame.draw.arc(screen,BLACK,[distance*(int(to_state[1:])+1), 225-(h/2), distance*abs_diff, h], 0, pi, 2)
                                screen.blit(text, [distance*(int(to_state[1:])+1) + distance*abs_diff/2+(w*10), 240-(h/2)])
                                
            
                            else:
                                pygame.draw.polygon(screen, BLACK, [[distance*(int(from_state[1:])+1) + distance*abs_diff/2, 335+(h/2)],
                                                                    [distance*(int(from_state[1:])+1) + distance*abs_diff/2, 315+(h/2)],
                                                                    [distance*(int(from_state[1:])+1)+8 + distance*abs_diff/2, 325+(h/2)]], 4)
                                pygame.draw.arc(screen,BLACK,[distance*(int(from_state[1:])+1), 225-(h/2), distance*abs_diff, h+100], pi, 0, 2)
                                screen.blit(text, [distance*(int(from_state[1:])+1) + distance*abs_diff/2+w, 290+(h/2)])
                        rs += 1
            pygame.display.flip()
        pygame.quit()

    def set_transition_dict(self):
        dict_states = {r: {c: 'ϕ' for c in self.states} for r in self.states}
        for i in range(len(self.states)):
            for j in range(len(self.states)):
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
