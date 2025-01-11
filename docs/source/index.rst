Conditional Parser
==================

A flexible extension to Python's ``ArgumentParser`` that enables dynamic, conditional command-line arguments - arguments that only appear based on the values of other arguments.

The argparse module is fantastic, but it lacks the ability to flexibly create conditional arguments. While the native ``ArgumentParser`` supports the ability to make a single subcommand, it does not have the ability to make multiple conditional arguments in parallel, in hierarchical structures, or with complex conditional logic. The ``ConditionalArgumentParser`` extends the native ``ArgumentParser`` to support these features while maintaining the familiar interface.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   quickstart
   examples/index
   api

Key Features
------------

* Seamless extension of Python's ArgumentParser
* Support for conditional arguments based on other argument values
* Hierarchical conditional dependencies
* Compatible with existing ArgumentParser usage
* Comprehensive help messages showing all possible arguments
* Clear documentation of when conditional arguments become available

Quick Example
-------------

Suppose your parser includes a ``--use-regularization`` flag for training a machine learning model. When this flag is used, you'd probably want to include another argument ``--regularizer-lambda`` to control the regularization strength - but this parameter is only relevant when regularization is enabled. With ``ConditionalArgumentParser``, you can easily add this conditional argument.

.. code-block:: python

    from conditional_parser import ConditionalArgumentParser

    parser = ConditionalArgumentParser()
    parser.add_argument("--use-regularization", action="store_true")
    
    # Will only add if --use-regularization is used
    # E.g. if args.use_regularization == True
    parser.add_conditional(
        "use_regularization", True, # parent / condition
        "--regularizer-lambda", # conditional argument
        # parameters for the conditional argument - these are totally normal!
        type=float, 
        default=0.01
    )

Design Note
-----------

This package does not work with subparsers. If you include a subparser, any conditional 
arguments will be ignored. I'm working on a solution for this, but it's not yet
implemented. Just note that if you need to use a subparser-like system, you can actually
completely replace subparsers with conditional arguments, the API just looks a bit
different. Here's an example:

.. code-block:: python

    parser = ArgumentParser()
    parser.add_argument("--no-subparsers-format", choices=["json", "csv"])
    subparsers = parser.add_subparsers()

    sub1 = subparsers.add_parser("command1")
    sub1.add_argument("--format", choices=["json", "csv"])

    # The above is (almost) equivalent to:
    parser = ConditionalArgumentParser()
    parser.add_argument("--no-subparsers-format", choices=["json", "csv"])
    parser.add_argument("--subparser", type=str, choices=["command1"], required=False)
    parser.add_conditional(
        "subparser",
        "command1",
        "--format",
        choices=["json", "csv"]
    )


