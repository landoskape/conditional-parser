Quick Start Guide
=================

Basic Usage
-----------

The ConditionalArgumentParser extends Python's ArgumentParser to allow arguments that only appear based on other argument values.

Here's a simple example:

.. code-block:: python

    from conditional_parser import ConditionalArgumentParser

    # Create parser just like ArgumentParser
    parser = ConditionalArgumentParser()
    
    # Add regular argument
    parser.add_argument("--use-regularization", 
                       action="store_true",
                       help="Uses regularization if included.")
    
    # Add conditional argument
    parser.add_conditional(
        dest="use_regularization",    # Which argument to check
        cond=True,                    # Condition to meet
        "--regularizer-lambda",       # Argument to add when condition is met
        type=float, 
        default=0.01,
        help="The lambda value for the regularizer."
    )

Adding Conditional Arguments
----------------------------

The key method is ``add_conditional``, which takes the following arguments:

1. ``dest``: The destination (argument name) to check. 
    The ``dest`` name is the same one that you would use to retrieve the argument value
    from the output of the parser. The nomenclature is intended to be consistent with
    argparse - when an argument is made in argparse, it is stored under the name
    designated in ``dest``.
    
    .. code-block:: python
        
        import ArgumentParser from argparse
        parser = ArgumentParser()
        parser.add_argument("--use-regularization", action="store_true", help="Uses regularization if included.")
        args = parser.parse_args(["--use-regularization"])

        # Argument parser will store the value of "--use-regularization"
        # in the namespace under the name "use_regularization"
        # This is what the ``dest`` argument refers to.
        args.use_regularization  # True
    
    So if you want to add a conditional argument that is only added when the
    ``--use-regularization`` argument is included, you would set ``dest="use_regularization"``.

2. ``cond``: The condition that ``dest`` has to meet for the conditional argument to be added. 
    Either a value to compare against or a callable function that accepts the value of the dest as it's single input argument and returns a boolean. 
3. Additional arguments passed to ``add_argument`` as usual. 
    These are the same arguments that you would pass to ``add_argument`` in argparse, and will be passed to the parser using parser.add_argument() whenever the condition is met.

Conditions can be:

* Simple equality: ``cond="value"``
* Boolean check: ``cond=True``
* Custom function: ``cond=lambda x: x in ["value1", "value2"]``

Help Messages
-------------

Help messages show all possible conditional arguments with information about when they become available:

.. code-block:: bash

    $ python script.py --help
    usage: script.py [-h] [--use-regularization] [--regularizer-lambda LAMBDA]

    optional arguments:
      -h, --help            show this help message and exit
      --use-regularization  Uses regularization if included.
      --regularizer-lambda  The lambda value for the regularizer. (Available when use_regularization=True)