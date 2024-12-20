Conditional Parser
=================

A flexible extension to Python's ArgumentParser for conditional arguments.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   examples/index
   api/index

About
-----

The Conditional Parser package extends Python's native ArgumentParser to enable dynamic, 
conditional command-line arguments - arguments that only appear based on the values of 
other arguments.

Key Features
-----------

* Seamless extension of Python's ArgumentParser
* Support for conditional arguments based on other argument values
* Hierarchical conditional dependencies
* Maintains helpful error messages and help text
* Compatible with existing ArgumentParser usage

Quick Example
------------

.. code-block:: python

    from conditional_parser import ConditionalArgumentParser

    parser = ConditionalArgumentParser()
    parser.add_argument("--use-regularization", action="store_true")
    
    parser.add_conditional(
        "use_regularization", True,
        "--regularizer-lambda", 
        type=float, 
        default=0.01
    )