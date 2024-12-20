Quick Start Guide
===============

Basic Usage
----------

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
-------------------------

The key method is ``add_conditional``, which takes:

1. ``dest``: The destination (argument name) to check
2. ``cond``: Either a value to compare against or a callable function
3. Additional arguments passed to ``add_argument``

Conditions can be:

* Simple equality: ``cond="value"``
* Boolean check: ``cond=True``
* Custom function: ``cond=lambda x: x in ["value1", "value2"]``

Help Messages
------------

Help messages automatically adjust to show only relevant arguments:

.. code-block:: bash

    # Without --use-regularization:
    $ python script.py --help
    usage: script.py [-h] [--use-regularization]

    # With --use-regularization:
    $ python script.py --use-regularization --help
    usage: script.py [-h] [--use-regularization] [--regularizer-lambda LAMBDA]