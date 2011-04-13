"""Library provides state machine to controll models

Example usage:


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

        state = StateProperty('default')

        default = State()
        working = State(state)
        waiting = State()

        Event(from_state=default, to_state=working)
        Event(from_state=default, to_state=waiting)
        Event(from_state=working, to_state=waiting, task=finish_task)

"""


class NoSuchStateException(Exception):
    """Exception called when there is no state for specified value
    """
    pass


class State(object):
    """State representation
    """

    def __init__(self, property=None, on_enter=None, on_exit=None):
        """Create new state for specified property name and value

        Arguments:
            name    property name
        """
        super(State, self).__init__()
        self.property   = property
        self.on_enter   = on_enter
        self.on_exit    = on_exit

    def enter(self, prev_state=None):
        """Enter the state
        """
        if self.on_enter is not None:
            self.on_enter(self.property, self.name, 
                          prev_state. self.property.get())

    def exit(self, next_state=None):
        if self.on_exit is not None:
            self.on_exit(self.property, self.name, 
                         self.property.get(), next_state)


class Event(object):
    """Event object representatin changing of the state
    """

    def __init__(self, obj, property, from_value, to_value, task):
        """Create new event instance

        Arguments:
            property    - property event on
            start       - start value for this event
            end         - end value for this event
        """
        self.obj        = obj
        self.property   = property
        self.from_value = from_value
        self.to_value   = to_value
        self.task       = task

    def __call__(self):
        if self.task is not None:
            self.task(obj, property, from_value, to_value)


class StateProperty(object):
    """Property used 
    """

    def __init__(self, obj, property, states=[]):
        """Create new state property for specified object property
        """
        self.obj        = obj
        self.property   = property
        self.states     = {[(state, State())]}
        self.events     = []

    def set(self, new_state):
        """Change state
        """
        old_state = obj.__dict__[property]
        # Process exit
        self.states[old_state].exit(new_state)
        # Process events
        for event in self.events:
            if event.from_value == old_state and event.to_value == new_state:
                event()
        # Process enter
        self.states[new_state].enter(new_state)


def add_state_properties(cls, property, initial_value):
    """Add new state property into list

    Arguments:
        property        original property
        initial_value   default value
    """
    # Get hidden properties
    properties_alias = '_%s__state_properties' % cls.__name__
    if properties_alias not in cls.__dict__:
        cls.__dict__[properties_alias] = {}
    properties = cls.__dict__[properties_alias]
    # Check for dublicate
    if isinstance(property, str) or issubclass(property.__class__, str):
        properties[property] = StateProperty()
    else:
        if '_uninitializaed_state_properties' not in cls.__dict__:
            cls.__dict__['_uninitializaed_state_properties'] = [property,]
        else:
            cls.__dict__['_uninitializaed_state_properties'].append(property)



def StateMachine(cls, **args):
    """Create class represents state machine
    """
    super_new = super(cls, cls).__new__
    # Get all
    new_atts = {cls.__dict__}
    states = {}
    events = {}
    for arg_name in args:
        arg = args[arg_name]
        if isinstance(arg, State) or issubclass(arg.__class__, State):
            states[arg_name] = arg
        elif isinstance(arg, Event) or issubclass(arg.__class__, Event):
            new_atts[attr_name] = attr
    new_atts['__states'] = states
    print new_atts
    return super_new(cls, name, bases, new_atts)
