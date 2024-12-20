Basic Example
============

This example shows the simplest use case for conditional arguments - adding an argument that only appears when a flag is set.

.. code-block:: python

    from conditional_parser import ConditionalArgumentParser

    # Create parser
    parser = ConditionalArgumentParser(description="A parser with conditional arguments.")
    
    # Add base argument
    parser.add_argument("--use-regularization", 
                       default=False, 
                       action="store_true", 
                       help="Uses regularization if included.")

    # Add conditional argument
    parser.add_conditional(
        "use_regularization",         # check this argument
        True,                         # when it's True
        "--regularizer-lambda",       # add this argument
        type=float, 
        default=0.01, 
        help="The lambda value for the regularizer."
    )

Usage Examples
-------------

Without regularization:

.. code-block:: bash

    $ python script.py
    Namespace(use_regularization=False)

With regularization:

.. code-block:: bash

    $ python script.py --use-regularization --regularizer-lambda 0.1
    Namespace(use_regularization=True, regularizer_lambda=0.1)

Error case (trying to set conditional without meeting condition):

.. code-block:: bash

    $ python script.py --regularizer-lambda 0.1
    error: unrecognized arguments: --regularizer-lambda 0.1