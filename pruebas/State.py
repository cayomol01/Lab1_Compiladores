


class State(object):
    def __init__(self, name:str = None, transitions:dict = None, token:str = None) -> None:
        self.transitions = transitions if transitions else {}
        self.name = name
        self.token = token
        
    def AddTransition(self,state, edge):
        if state in self.transitions:
            self.transitions[state] = [self.transitions[state]]
            self.transitions[state].append(edge)
        else:
            self.transitions[state] = edge
            
    def GetTransitions(self):
        return self.transitions
    
    def GetTransitionStates(self):
        states = set()
        
        if self.transitions:
            for key,value in self.transitions.items():
                states.add(key)
            return states
        else:
            return None
        
