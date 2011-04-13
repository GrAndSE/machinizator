from machinizator import *

class Test:
    name = "Andy"
    state = None


def finish_task(obj, name, from_state, to_state):
    print "Finish task"
    print obj, name, from_state, to_state

def start_task(obj, name, from_state, to_state):
    print "Start task"
    print obj, name, from_state, to_state       


class TestStateMachine(StateMachine):
    for_class = Test

    state = StateProperty()

    default = State(state)
    working = State(state)
    waiting = State(state)

    state.init_with(default)

    Event(from_state=default, to_state=working)
    Event(from_state=default, to_state=waiting)
    Event(from_state=working, to_state=waiting, task=finish_task)
