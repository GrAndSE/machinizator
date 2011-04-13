"""Library provides state machine to controll models
"""


class NoSuchStateException(Exception):
    """Exception called when there is no state for specified value
    """
    pass


class State(object):
    """State representation
    """

    def __init__(self, name, value, 
                        on_enter=None, on_exit=None,
                        restrictions=None):
        """Create new state for specified property name and value
        """
        super(State, self).__init__()
        self.name   = name
        self.value  = value


class Event(object):
    """Event object representatin changing of the state
    """

    def __init__(self, property, from_value, to_value, task):
        """Create new event instance

        Arguments:
            property    - property event on
            start       - start value for this event
            end         - end value for this event
        """
        self.property   = property
        self.from_value = start
        self.to_value   = end
        self.task       = task


class StateProperty(object):
    """Property used 
    """

    def __init__(self, obj, property):
        """Create new state property for specified object property
        """
        self.property   = property
        self.obj        = obj
        self.states     = {}
        self.events     = []

    def set(self, value):
        """Chane
        """


class StateMachineBase(type):
    """Metaclass for all the state machine classes
    """

    def __new__(cls, name, bases, attrs):
        """Create new class
        """
        super_new = super(StateMachineBase, cls).__new__
        parents = [b for b in bases if isinstance(b, StateMachineBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        # Get all

        return


class StateMachine(object):
    """Class representing the state machine
    """
    __metaclass__ = StateMachineBase

    def __setattr__(self, name, value):
        """Set attribute with state switching
        """
        if name is self.__states:
            self.__states[name].set(value)
        else:
            super(StateMachine, self).__setattr__(name, value)
