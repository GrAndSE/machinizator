"""Library provides state machine to controll models

Example usage:


    class Test:
        name = "Andy"
        state = None


    def finish_task(from_state, to_state):
        print "Finish task"
        print from_state, to_state

    def start_task(from_state, to_state):
        print "Start task"
        print from_state, to_state       


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


class UnconfiguredStateException(Exception):
    """Exception raised when trying to enter into state or exit from state 
    which was not configured properly
    """
    pass


class UnconfiguredStatePropertyException(Exception):
    """Exception raised when init_with(state) method of the StateProperty 
    instance was not called and instance was created with no specified initial
    argument value
    """
    pass


class NoSuchStateException(Exception):
    """Exception called when there is no state for specified value
    """
    pass


class State(object):
    """State representation
    """

    def __init__(self, property=None, state=None, 
                 on_enter=None, on_exit=None):
        """Create new state for specified property name and value

        Arguments:
            name    property name
        """
        super(State, self).__init__()
        self.state      = state
        self.on_enter   = on_enter
        self.on_exit    = on_exit

    def enter(self, prev_state=None):
        """Enter the state
        """
        if self.on_enter is not None:
            self.on_enter(self.property.obj, self.property.name,
                          prev_state, self.state)

    def exit(self, next_state=None):
        """Exit the state
        """
        self.check_configured()
        if self.on_exit is not None:
            self.on_exit(self.property.obj, self.property.name,
                         self.state, next_state)

    def check_configured(self):
        """
        """
        if self.state is None:
            raise UnconfiguredStateProperty


class Event(object):
    """Event object representatin changing of the state
    """

    def __init__(self, from_state, to_state, task=None):
        """Create new event instance

        Arguments:
            property    - property event on
            start       - start value for this event
            end         - end value for this event
        """
        self.from_state = from_state
        self.to_state   = to_state
        self.task       = task

    def __call__(self):
        if self.task is not None:
            self.task(from_state, to_state)


class StateProperty(object):
    """Property used 
    """

    def __init__(self, initial=None, property=None, states=[], events=[]):
        """Create new state property for specified object property
        """
        self.obj        = None
        self.initial    = initial
        self.property   = property
        self.states     = {tuple((state, State(property=self, state=state)) 
                                 for state in states)}
        self.events     = events

    def set(self, new_state):
        """Change state
        """
        # Process exit
        old_state = obj.__dict__[property]
        self.states[old_state].exit(new_state)
        # Process events
        for event in self.events:
            if (event.from_state.state == old_state and 
                event.to_state.state == new_state):
                event()
        # Process enter
        self.states[new_state].enter(new_state)
        obj.__dict__[property] = new_state

    def init_with(self, initial):
        """Change initial state for this property
        """
        self.initial = initial

    def finish_init(self, obj, property):
        """Finish property initialization
        """
        if self.initial is None:
            raise UnconfiguredStateProperty()
        self.obj = obj
        self.property = property
        obj.__dict__[property] = self.initial


class StateMachineBase(type):
    """Metaclass for each StateMachine subclasses
    """

    def __new__(cls, name, bases, attrs):
        super_new = super(cls, cls).__new__
        parents = [b for b in bases if isinstance(b, StateMachineBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        # Get all
        if 'for_class' not in attrs:
            raise Exception() # TODO: generate good exceptio
        for_class = attrs['for_class']
        new_atts = {}
        new_atts.update()
        del attrs['for_class']
        states = {}
        events = {}
        for attr_name in attrs:
            attr = attrs[attr_name]
            if isinstance(attr, State) or issubclass(attr.__class__, State):
                attr.state = attr_name
                states[attr_name] = attr
            elif isinstance(attr, Event) or issubclass(attr.__class__, Event):
                new_atts[attr_name] = attr
        new_atts['__states'] = states
        print new_atts
        return super_new(cls, name, bases, new_atts)


class StateMachine(object):
    """Create class represents state machine
    """
    __metaclass__ = StateMachineBase

    def __init__(self):
        """Create new StateMachine instance. Just inherit from parent
        """
        super(StateMachine, self).__init__()
