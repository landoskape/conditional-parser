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
