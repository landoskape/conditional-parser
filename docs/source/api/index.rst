API Reference
============

ConditionalArgumentParser
------------------------

.. autoclass:: conditional_parser.ConditionalArgumentParser
   :show-inheritance:
   :special-members: __init__
   :members: add_conditional, parse_args
   :private-members: _
   

The ConditionalArgumentParser extends Python's ArgumentParser to support conditional
arguments. It inherits all standard ArgumentParser functionality while adding the ability
to specify arguments that only appear when certain conditions are met.

Key Methods
----------

The main addition to ArgumentParser is the :meth:`add_conditional` method, which allows
you to add a conditional argument to the parser. This method takes the same arguments as
the standard :meth:`add_argument` method, with the addition of a `dest` and `cond`
arguments which specify the destination in the namespace to check for the condition and
the condition itself, respectively.

add_conditional
~~~~~~~~~~~~~~
.. automethod:: conditional_parser.ConditionalArgumentParser.add_conditional
