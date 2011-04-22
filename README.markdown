Machinizator
===============

Machinizator is a library for Python can be used to build a state machines from
already defined objects. You can just write another class described state 
machine around exists object fileds and replace old class with newly created. 
This state machine class get all fields from wrapped class and adds new 
functionality to control current object state.

Supports:
---------

- Pure python
- DSL for state machine creation.
- Change state events with callbacks
- Calbacks on state enter or exit

Example:
--------

See test.py for working example.

TODO:
-----

- Write more tests.
- Add setup-tools support.
- Think how can we made single state machine from few different objects (useful
to keep relations between object states)
