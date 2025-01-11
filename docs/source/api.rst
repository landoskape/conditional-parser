API Reference
=============

ConditionalArgumentParser
-------------------------

.. autoclass:: conditional_parser.ConditionalArgumentParser
   :show-inheritance:
   :special-members: __init__
   :members: add_conditional, parse_args
   

The ConditionalArgumentParser extends Python's ArgumentParser to support conditional
arguments. It inherits all standard ArgumentParser functionality while adding the ability
to specify arguments that only appear when certain conditions are met.

Key Methods
-----------

The main addition to ArgumentParser is the :meth:`add_conditional` method, which allows you to add a conditional argument to the parser. This method takes the same arguments as the standard :meth:`add_argument` method, with the addition of a `dest` and `cond` arguments which specify the destination in the namespace to check for the condition and the condition itself, respectively. 

.. note::
   The ``dest`` argument is the name of the argument in the namespace that will be checked for the condition. The nomenclature might be a bit confusing; it's used to be consistent with how the ``ArgumentParser`` assigns arguments to the namespace. 
   
   What you are looking for is whatever attribute name you'd use to get the value of the argument from the output of ``parse_args()``. So, for example:
   
   .. code-block:: python
        
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument("--use-regularization", default=False, action="store_true")
        parser.add_argument("--nohyphen", default=False, action="store_true")
        args = parser.parse_args(["--use-regularization"])
        # The "dest" of --use-regularization is "use_regularization"
        print(args.use_regularization) # True
        # The "dest" of --nohyphen is "nohyphen"
        print(args.nohyphen) # False

Internal Methods
---------------

The following methods are used internally by ConditionalArgumentParser to manage conditional arguments:

.. py:method:: _prepare_conditionals(_parser, args, already_added)

   Recursively prepare and add conditional arguments to the parser based on the values of their parent arguments.

   :param ArgumentParser _parser: The parser to which conditional arguments will be added
   :param List[str] args: List of command line arguments to parse
   :param List[bool] already_added: List tracking which conditional arguments have already been added
   :return: The parser with all required conditional arguments added
   :rtype: ArgumentParser

.. py:method:: _prepare_help(_parser)

   Prepare the help parser to show all conditional arguments in the help output with modified help text.

   :param ArgumentParser _parser: The parser to which help text will be added
   :return: The parser with all conditional arguments and their help text added
   :rtype: ArgumentParser

.. py:method:: _make_callable(cond)

   Convert a condition into a callable function.

   :param Union[Callable, Any] cond: Either a callable or a value to compare against
   :return: A function that takes one argument and returns a boolean
   :rtype: Callable
   :raises ValueError: If cond is callable but doesn't accept exactly one argument

.. py:method:: _callable_representation(parent, cond)

   Get a string representation of a condition for help text.

   :param str parent: The destination name of the parent argument
   :param Union[Callable, Any] cond: The condition to represent
   :return: A string describing when the conditional argument is available
   :rtype: str

.. py:method:: _conditionals_ready(namespace, already_added)

   Check if all required conditional arguments have been added to the parser.

   :param Namespace namespace: The namespace containing the current parsed arguments
   :param List[bool] already_added: List tracking which conditional arguments have been added
   :return: True if all required conditional arguments have been added
   :rtype: bool

.. py:method:: _conditional_required(namespace, parent, already_added, idx)

   Check if a specific conditional argument needs to be added.

   :param Namespace namespace: The namespace containing the current parsed arguments
   :param str parent: The destination name of the parent argument
   :param List[bool] already_added: List tracking which conditional arguments have been added
   :param int idx: Index of the conditional argument being checked
   :return: True if the conditional argument needs to be added
   :rtype: bool


