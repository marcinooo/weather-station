
class State:
    name: None

    def run(self, machine):
        raise NotImplementedError()

    def error(self, machine):
        raise NotImplementedError()

    def update(self, machine):
        raise NotImplementedError()
        

class StateMachine(object):

    def __init__(self):
        self.state = None
        self.states = {}
        self.context = {}

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        self.state = self.states[state_name]
        self.state.run(self)

    def update(self):
        if self.state:
            self.state.update(self)
