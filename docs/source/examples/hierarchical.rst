Hierarchical Conditionals
=======================

This example shows how to create nested conditional arguments, where one conditional argument can trigger additional conditional arguments.

.. code-block:: python

    from conditional_parser import ConditionalArgumentParser

    parser = ConditionalArgumentParser()

    # Top-level argument
    parser.add_argument("--use-curriculum", 
                       default=False, 
                       action="store_true",
                       help="Use curriculum for training.")

    # First-level conditional (activated when '--use-curriculum' is set)
    parser.add_conditional("use_curriculum", True,
                         "--curriculum", type=str, required=True,
                         help="Which curriculum to use")

    # Second-level conditional for curriculum1 (activated when '--curriculum' is "curriculum1")
    parser.add_conditional("curriculum", "curriculum1",
                         "--curriculum1-prm1", type=int, required=True,
                         help="Parameter 1 for curriculum1")
    parser.add_conditional("curriculum", "curriculum1",
                         "--curriculum1-prm2", type=int, required=True,
                         help="Parameter 2 for curriculum1")

    # Second-level conditional for curriculum2 (activated when '--curriculum' is "curriculum2")
    parser.add_conditional("curriculum", "curriculum2",
                         "--curriculum1-prm2", type=int, default=128,
                         help="Parameter A for curriculum2")
    parser.add_conditional("curriculum", "curriculum2",
                         "--curriculum1-prm2", type=int, default=128,
                         help="Parameter B for curriculum2")

Understanding the Hierarchy
-------------------------

1. ``--use-curriculum`` is the top-level flag
2. When True, it enables the ``--curriculum`` argument
3. When ``--curriculum`` is "curriculum1", it enables curriculum1-specific parameters
4. When ``--curriculum`` is "curriculum2", it enables curriculum2-specific parameters

This creates a tree of dependencies:

.. code-block:: text

    --use-curriculum
        └── --curriculum
            ├── curriculum1
            │   ├── --curriculum1-prm1
            │   └── --curriculum1-prm2
            └── curriculum2
                ├── --curriculum2-prmA
                └── --curriculum2-prmB