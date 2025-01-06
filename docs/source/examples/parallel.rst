This example demonstrates using multiple conditional arguments in parallel, triggered by different values of the same parent argument.

.. code-block:: python

    from conditional_parser import ConditionalArgumentParser

    parser = ConditionalArgumentParser()

    # Base argument that controls multiple sets of conditionals
    parser.add_argument("dataset", type=str, 
                       help="Which dataset to use for training/testing.")

    # Dataset1-specific parameters
    parser.add_conditional("dataset", "dataset1",
                         "--dataset1-prm1", type=int,
                         help="Parameter 1 for dataset1")
    parser.add_conditional("dataset", "dataset1",
                         "--dataset1-prm2", type=int,
                         help="Parameter 2 for dataset1")

    # Dataset2-specific parameters
    parser.add_conditional("dataset", "dataset2",
                         "--dataset2-prmA", type=str,
                         help="Parameter A for dataset2")
    parser.add_conditional("dataset", "dataset2",
                         "--dataset2-prmB", type=str,
                         help="Parameter B for dataset2")

    # Parameters shared between dataset3 and dataset4
    parser.add_conditional("dataset", 
                         lambda d: d in ["dataset3", "dataset4"],
                         "--datasets34-prmX", type=str,
                         help="Parameter X for datasets 3 and 4")

Key Features Demonstrated

* Multiple conditionals can depend on the same parent argument
* Different values of the parent can trigger different conditionals
* Lambda functions allow complex conditional logic
* Conditionals can be shared across multiple values