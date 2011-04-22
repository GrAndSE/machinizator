"""Library provides state machine to controll models

Example usage:


    class Test:
        name = "Andy"
        state = None


    def finish_task(obj, from_state, to_state):
        print "Finish task"
        print from_state, to_state

    def start_task(obj, from_state, to_state):
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
        self.property   = property
        if state is not None:
            property.states[state] = self

    def enter(self, obj, prev_state=None):
        """Enter the state
        """
        self.check_configured()
        if self.on_enter is not None:
            self.on_enter(obj, prev_state, self.state)

    def exit(self, obj, next_state=None):
        """Exit the state
        """
        self.check_configured()
        if self.on_exit is not None:
            self.on_exit(obj, self.state, next_state)

    def check_configured(self):
        """Check is State properly configured
        """
        if self.state is None:
            raise UnconfiguredStatePropertyException()

    def __str__(self):
        """Get a straing representation
        """
        return "%s: %s" % (self.property.property, self.state)


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
        # Add event to state property
        self.from_state.property.events.append(self)

    def __call__(self, obj):
        if self.task is not None:
            self.task(obj, self.from_state.property.property,  
                      self.from_state, self.to_state)


class StateProperty(object):
    """Property used 
    """

    def __init__(self, initial=None, property=None, states=[], events=[]):
        """Create new state property for specified object property
        """
        self.obj        = None
        self.initial    = initial
        self.property   = property
        self.states     = dict(((state, State(property=self, state=state)) 
                                 for state in states))
        self.events     = events

    def set(self, obj, new_state):
        """Change state
        """
        # Process exit
        old_state = obj.__dict__[self.property]
        self.states[old_state].exit(new_state)
        # Process events
        for event in self.events:
            if (event.from_state.state == old_state and 
                event.to_state.state == new_state):
                event(obj)
        # Process enter
        self.states[new_state].enter(new_state)
        obj.__dict__[self.property] = new_state

    def init_with(self, initial):
        """Change initial state for this property
        """
        self.initial = initial

    def finish_init(self, obj, property):
        """Finish property initialization
        """
        if self.initial is None:
            raise UnconfiguredStatePropertyException()
        self.property = property
        obj.__dict__[property] = self.initial.state


class StateMachineBase(type):
    """Metaclass for each StateMachine subclasses
    """

    def __new__(cls, name, bases, attrs):
        """Create new class from StateMachine and for_class argument:

        Get all properties and methods from for_class and add states and 
        methods to access the states
        """
        def is_state(state):
            return lambda self: self.state == state

        super_new = super(cls, cls).__new__
        parents = [b for b in bases if isinstance(b, StateMachineBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        # Get class updated to state machine
        if 'for_class' not in attrs:
            raise Exception() # TODO: generate good exceptio
        for_class = attrs['for_class']
        new_attrs = {}
        new_attrs.update(for_class.__dict__)
        del attrs['for_class']
        # Get states, properties, events and fields from state machine class
        states = {}
        events = {}
        properties = {}
        for attr_name in attrs:
            attr = attrs[attr_name]
            if isinstance(attr, State) or issubclass(attr.__class__, State):
                attr.state = attr_name
                states[attr_name] = attr
                new_attrs['is_%s' % attr_name] = is_state(attr_name)
            elif isinstance(attr, Event) or issubclass(attr.__class__, Event):
                events[attr_name] = attr
            elif (isinstance(attr, StateProperty) or 
                    issubclass(attr.__class__, StateProperty)):
                properties[attr_name] = attr
            else:
                new_attrs[attr_name] = attr
        # Apply states to state properties
        for state_name in states:
            state = states[state_name]
            state.property.states[state.state] = state
        # Apply events to states
        for event_name in events:
            event = events[event_name]
            event
        # Put all into new class attributes
        new_attrs['_StateMachine__states'] = states
        new_attrs['_StateMachine__events'] = events
        new_attrs['_StateMachine__properties'] = properties
        return super_new(cls, name, bases, new_attrs)


class StateMachine(object):
    """Create class represents state machine
    """
    __metaclass__ = StateMachineBase

    def __init__(self, *args, **kwargs):
        """Create new StateMachine instance. Just inherit from parent
        """
        super(StateMachine, self).__init__(*args, **kwargs)
        # Finish properties initlization
        for property in self.__properties:
            self.__properties[property].finish_init(self, property)

    def __setattr__(self, name, value):
        """Check is trying to modify a state property name and for state
        property run full procedure
        """
        if name in self.__properties:
            self.__properties[name].set(self, value)
        else:
            super(StateMachine, self).__setattr__(name, value)
