import pygame
import pygame.gfxdraw

class NFA:
    def __init__(self, states, terminals, transitions, finalStates):
        self.states = states
        self.terminals = terminals
        self.transitions = transitions
        self.finalStates = finalStates

    def IsAcceptByNFA(self, firstState, s):
        result = False
        if(len(s) == 0):
            if(firstState in self.finalStates):
                return True
            else:
                return False
        else:
            for t in self.transitions:
                if t[0] == firstState and t[2] == s[0] and result == False:
                    result = self.IsAcceptByNFA(t[1], s[1:len(s)])
                elif t[0] == firstState and t[2] == 'landa' and result == False:
                    result = self.IsAcceptByNFA(t[1], s[0:len(s)])
            return result
        return result

    def FindRegex(self):
        # equalDFA=self.CreateEqeulvantDFA
        # return equalDFA.FindRegex()
        pass

    def CreateEqeulvantDFA(self):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
        state_alph = {}
        new_finalstates = []
        new_states = []
        new_transitions = []
        self.terminals.append('landa')
        for i in range(len(self.states)):
            state_alph[(self.states)[i]] = alphabet[i]
            new_states.append(alphabet[i])
        for tr in self.transitions:
            temp = []
            temp.append(state_alph[tr[0]])
            temp.append(state_alph[tr[1]])
            temp.append(tr[2])
            new_transitions.append(temp)
        for j in range(len(self.finalStates)):
            new_finalstates.append(state_alph[(self.finalStates)[j]])

        nfa = {}
        states_num = len(new_states)
        transition_num = len(new_transitions)
        for i in range(states_num):
            state = new_states[i]
            nfa[state] = {}
            for terminal in self.terminals:
                nfa[state][terminal] = []
                for j in range(transition_num):
                    if new_transitions[j][0] == state and new_transitions[j][2] == terminal:
                        nfa[state][terminal].append(new_transitions[j][1])
    
        new_states_list = []
        keys_list = list(list(nfa.keys()))
        path_list = self.terminals

        for k in range(len(keys_list)):
            key = keys_list[k]
            if len(nfa[key]['landa']) != 0:
                for transition in new_transitions:
                    if transition[1] == key:
                        for j in nfa[key]['landa']:
                            (nfa[transition[0]][transition[2]]).append(j)
        dfa = {}
        for i in range(len(keys_list)):
            key = keys_list[i]
            dfa[key] = {}
            for y in range(len(path_list)):
                var = ''
                if path_list[y] != 'landa':
                    if nfa[key][path_list[y]] != []:
                        for i in nfa[key][path_list[y]]:
                            var += i
                        for char in list(var):
                            if var.count(char) > 1:
                                var = var.replace(char, '', 1)
                        var = sorted(var)
                        var = "".join(var)
                        if var not in keys_list:
                            new_states_list.append(var)
                            keys_list.append(var)
                        dfa[key][path_list[y]] = var    
                else:
                    if nfa[key][path_list[y]] != []:
                        new_key = nfa[key][path_list[y]][0]
                        for p in range(len(path_list)):
                            if path_list[p] != 'landa':
                                if nfa[new_key][path_list[p]] != []:
                                    for i in nfa[new_key][path_list[p]]:
                                        var += i
                                    for char in list(var):
                                        if var.count(char) > 1:
                                            var = var.replace(char, '', 1)        
                                    for l in nfa[key][path_list[y]]:
                                        var += l
                                    var = sorted(var)
                                    var = "".join(var)        
                                    if var not in keys_list:
                                        new_states_list.append(var)
                                        keys_list.append(var)
                                    dfa[key][path_list[y]] = var


        while len(new_states_list) != 0:
            dfa[new_states_list[0]] = {}
            for y in range(len(path_list)):
                var = ''
                if path_list[y] != 'landa':
                    for j in range(len(new_states_list[0])):  
                        if nfa[new_states_list[0][j]][path_list[y]] != []:
                            for i in nfa[new_states_list[0][j]][path_list[y]]:
                                var += i
                            for char in list(var):
                                if var.count(char) > 1:
                                    var = var.replace(char, '', 1)
                            var = sorted(var)
                            var = "".join(var)
                            if var not in keys_list:
                                new_states_list.append(var)
                                keys_list.append(var)
                            dfa[new_states_list[0]][path_list[y]] = var
                else:
                    for j in range(len(new_states_list[0])):
                        if nfa[new_states_list[0][j]][path_list[y]] != []:
                            new_key = nfa[new_states_list[0][j]][path_list[y]][0]
                            for p in range(len(path_list)):
                                if path_list[p] != 'landa':
                                    if nfa[new_key][path_list[p]] != []:
                                        for i in nfa[new_key][path_list[p]]:
                                            var += i
                                        for char in list(var):
                                            if var.count(char) > 1:
                                                var = var.replace(char, '', 1)
                                        var = sorted(var)
                                        var = "".join(var)        
                                        if var not in keys_list:
                                            new_states_list.append(var)
                                            keys_list.append(var)   
                                        dfa[new_states_list[0][j]][path_list[p]] = var
            new_states_list.remove(new_states_list[0])

        new_path_list = path_list[:-1]
        keys_list.append('X')
        for key in dfa.keys():
            for path in new_path_list:
                if path not in dfa[key].keys():
                    dfa[key][path] = 'X'
        
        for key in dfa.keys():
            flag = True
            i = 0
            while flag and i != len(path_list):
                if path_list[i] in dfa[key].keys():
                    if path_list[i] == 'landa':
                        del dfa[key][path_list[i]]
                        flag = False
                i += 1
        
        final_states_list = []
        for key in dfa.keys():
                for path in new_path_list:
                    if dfa[key][path] not in final_states_list:
                        final_states_list.append(dfa[key][path])

        dfa['X'] = {}
        for path in new_path_list:
            dfa['X'][path] = 'X'
        
        for key in dfa.keys():
            for c in key:
                if c in new_finalstates and key not in new_finalstates:
                    new_finalstates.append(key)
        
        self.new_finalstates = new_finalstates

        return dfa


    def Shape(self):
        self.terminals.append('landa')
        nfa = {}
        for i in range(len(self.states)):
            state = self.states[i]
            nfa[state] = {}
            for terminal in self.terminals:
                nfa[state][terminal] = []
                for j in range(len(self.transitions)):
                    if self.transitions[j][0] == state and self.transitions[j][2] == terminal:
                        nfa[state][terminal].append(self.transitions[j][1])
        
        for key in nfa.keys():
                for path in self.terminals:
                    if nfa[key][path] == []:
                        del nfa[key][path]
            

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
            for key in nfa.keys():
                pygame.draw.circle(screen, RED, [(distance*(int(key[1:])+1)), 250], r, 0)
                pygame.draw.circle(screen, BLUE, [(distance*(int(key[1:])+1)), 250], r-4, 0)
                font = pygame.font.SysFont(None, r+2)
                text = font.render((key), True, BLACK)
                screen.blit(text, [(distance*(int(key[1:])+1))-10, 240])
            
            pi = 3.14
            i = 0  
            for st in nfa.keys():
                same_path = []
                if st in self.finalStates:
                    pygame.draw.arc(screen,BLUE,[distance*(i+1)-27, 223, r*2+4, r*2+4], -3.3, 3, 4)
                i += 1
                w = 0
                for path in nfa[st].keys():
                    from_state = st
                    to_state = nfa[st][path]
                    diff = int(from_state[1:]) - int(to_state[w][1:])
                    abs_diff = abs(diff)
                    h = abs_diff * 100
                    font = pygame.font.SysFont(None, r+2)
                    if len(same_path) != 0 and nfa[st][same_path[0]] == nfa[st][path]:
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
                        screen.blit(text, [distance*(int(to_state[0][1:])+1)+20+(w*10), 315])
                    else:
                        if diff > 0:
                            pygame.draw.polygon(screen, BLACK, [[distance*(int(to_state[0][1:])+1) + distance*abs_diff/2, 235-(h/2)],
                                                                [distance*(int(to_state[0][1:])+1) + distance*abs_diff/2, 215-(h/2)],
                                                                [distance*(int(to_state[0][1:])+1)-8 + distance*abs_diff/2, 225-(h/2)]], 4)
                            pygame.draw.arc(screen,BLACK,[distance*(int(to_state[0][1:])+1), 225-(h/2), distance*abs_diff, h], 0, pi, 2)
                            screen.blit(text, [distance*(int(to_state[0][1:])+1) + distance*abs_diff/2+(w*10), 240-(h/2)])
                            
        
                        else:
                            pygame.draw.polygon(screen, BLACK, [[distance*(int(from_state[1:])+1) + distance*abs_diff/2, 335+(h/2)],
                                                                [distance*(int(from_state[1:])+1) + distance*abs_diff/2, 315+(h/2)],
                                                                [distance*(int(from_state[1:])+1)+8 + distance*abs_diff/2, 325+(h/2)]], 4)
                            pygame.draw.arc(screen,BLACK,[distance*(int(from_state[1:])+1), 225-(h/2), distance*abs_diff, h+100], pi, 0, 2)
                            screen.blit(text, [distance*(int(from_state[1:])+1) + distance*abs_diff/2+w, 290+(h/2)])
                

            pygame.display.flip()

        pygame.quit()

