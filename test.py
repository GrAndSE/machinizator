from machinizator import Event, State, StateMachine, StateProperty

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

    begining_start_task = Event(from_state=default, to_state=working)
    begining_wait_task = Event(from_state=default, to_state=waiting,
                               task=start_task)
    end_task_and_wait = Event(from_state=working, to_state=waiting, 
                              task=finish_task)

test_machine = TestStateMachine()
assert test_machine.is_default(), 'Default was not sent as initial value'
test_machine.state = 'waiting'
assert not test_machine.is_default(), 'Waiting requires is_default() == False'
assert test_machine.is_waiting(), 'Waiting requires is_waiting() == True'
test_machine.state = 'working'
assert not test_machine.is_waiting() and test_machine.is_working(), 'E:working'
test_machine.state = 'waiting'
assert test_machine.is_waiting() and not test_machine.is_working(), 'E:working'
