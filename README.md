# conditional-parser
A simple extension to the native ArgumentParser to allow flexible conditional arguments.  

[![PyPI version](https://badge.fury.io/py/conditional-parser.svg)](https://badge.fury.io/py/conditional-parser)

The argparse module is fantastic. I love it. However, it is lacking in one particular area: the ability to
flexibily create conditional arguments. 

What do I mean by conditional arguments? I mean the inclusion of certain arguments that are only necessary
given the values provided by the user for other arguments. For example, suppose you include a non-positional
argument like: ``--use-regularization`` for a parser build to train a machine learning model. You might want
to include another argument: ``--regularizer-lambda`` that determines how much regularization to use, but
only when the user includes the ``--use-regularization`` argument. This is a simple example, but it's easy to
imagine this being extend to much more complex use cases, and even hierarchically nested conditionals. 

The ``ConditionalArgumentParser`` contained in this package extends python's native ``ArgumentParser``. It
works almost identically, but allows the addition of conditional arguments in an intuitive and simple way.
In addition, the way ``ConditionalArgumentParser`` is structured maintains the usefulness of ``-help`` 
messages such that users can receive precisely the help that is relevant given any conditionals they provide. 

For more information, check it out at the GitHub repository: 
https://github.com/landoskape/conditional-parser/

## Installation
It's on PyPI. If there's any issues, please raise one on this GitHub repo to let me know.
```
pip install conditional-parser
```

## How it works
The ``ConditionalArgumentParser`` works just like a standard ``ArgumentParser``, except that it stores 
conditional arguments and adds them whenever necessary based on the arguments that are provided. The way it 
does this is simple: 

First, the user registers conditional arguments by indicating:
- What condition must be met for them to be added.
- What argument to be added if the condition is met. 

The user can add as many of these as they want, with arbitrary complexity and hierarchical levels. 

When the standard ``parse_args()`` method is called, it builds a namespace from the given arguments, checks
whether conditions are met, adds necessary conditional arguments, then does this again recursively until no
more conditional arguments are needed. In addition, it will ignore ``-h`` or ``--help`` arguments until all 
required conditional arguments are added such that the user receives an accurate and fully informative help
message given any of the conditionals they set.   

### How to add a conditional argument
To add a conditional argument, use the ``add_conditional`` method:

``add_conditional(self, dest, cond, *args, **kwargs):``

This method takes two positional arguments that determine which conditions require this argument to be added
to the parser and additional ``*args`` and ``**kwargs`` which are used to make the argument when required. 

1. ``dest``: Corresponds to the attribute name of the namespace on which to check the condition.
2. ``cond``: Either a value to compare ``namespace.dest`` to or a callable to run on ``namespace.dest``
             that returns a boolean. If not callable, then this conditional argument will be added when
             ``namespace.dest==cond``, where namespace.dest is created without the conditional arguments,
             then recreated with any required conditionals. If ``cond`` is callable, then this conditional
             argument will be added whenever ``cond(namespace.dest)`` returns ``True``.
             
             This process is repeated recursively until all necessary conditionals are added to handle
             potential hierarchical dependencies. 

3. ``*args``: Passed to ``add_argument`` to add the conditional argument when its condition is met.
4. ``**kwargs``: Passed to ``add_argument`` to add the conditional argument when its condition is met. 


## Usage
The [examples](https://github.com/landoskape/conditional-parser/tree/main/examples) folder has several
examples with permutations on how they can be used. See that for example usage and testing or building off of
existing examples. 

### Simple example of adding a conditional argument
This simple example shows how to implement the conditional parser described in the first section above. This
example corresponds to [readme_example](https://github.com/landoskape/conditional-parser/blob/main/examples/readme_example.py).
```python
# Build a conditional argument parser (identical to ArgumentParser)
parser = ConditionalArgumentParser(description="A parser with conditional arguments.")

# Add an argument
parser.add_argument("--use-regularization", default=False, action="store_true", help="Uses regularization if included.")

# Add a conditional argument that is only included when use_regularization=True
dest = "use_regularization"
cond = True
parser.add_conditional(dest, cond, "--regularizer-lambda", type=float, default=0.01, help="The lambda value for the regularizer.")

# Use the parser (--use-regularization will cause --regularizer-lambda to be added, so it can be set in the args)
args = ["--use-regularization", "--regularizer-lambda", "0.1"]
parsed_args = parser.parse_args(args=args)
```

### Parallel conditionals
This example shows how to implement a conditional parser with multiple conditional arguments in parallel. It 
also shows how to use callable conditionals for more complex control of when to add conditional arguments. 
This example corresponds to [parallel_example](https://github.com/landoskape/conditional-parser/blob/main/examples/parallel_example.py).
```python
# Build a conditional argument parser (identical to ArgumentParser)
parser = ConditionalArgumentParser(description="A parser with parallel conditional arguments.")

# Add an argument determining which dataset to use
parser.add_argument("dataset", type=str, required=True, help="Which dataset to use for training/testing.")

# Add conditionals that are only needed for dataset1
dest = "dataset"
condition = "dataset1"
parser.add_conditional(dest, condition, "--dataset1-prm1", help="prm1 for dataset1")
parser.add_conditional(dest, condition, "--dataset1-prm2", help="prm2 for dataset1")

# Add conditionals that are only needed for dataset2
dest = "dataset"
condition = "dataset2"
parser.add_conditional(dest, condition, "--dataset2-prmA", help="prmA for dataset2")
parser.add_conditional(dest, condition, "--dataset2-prmB", help="prmB for dataset2")

# Add conditionals that are needed for both datasets 3 and 4, but not the other datasets
dest = "dataset"
condition = lambda dest: dest in ["dataset3", "dataset4"]
parser.add_conditional(dest, condition, "--datasets34-prmX", help="prmX for datasets 3 and 4")
parser.add_conditional(dest, condition, "--datasets34-prmY", help="prmY for datasets 3 and 4")


# Add an argument determining which kind of network to use
parser.add_argument("--network-type", type=str, default="mlp", help="Which type of network to use for training/testing.")

# Add conditionals that are only needed for mlps
dest = "network_type"
condition = "mlp"
parser.add_conditional(dest, condition, "--mlp-layers", type=int, default=2, help="the number of mlp layers")
parser.add_conditional(dest, condition, "--mlp-layer-width", type=int, default=128, help="the width of each mlp layer")

# Add conditionals that are only needed for transfomers
dest = "network_type"
condition = "transfomer"
parser.add_conditional(dest, condition, "--num-heads", type=int, default=8, help="the number of heads to use in transfomer layers")
parser.add_conditional(dest, condition, "--kqv-bias", default=False, action="store_true", help="whether to use bias in the key/query/value matrices of the transfomer")
# ... etc.

# Use the parser 
args = ["dataset1", "--dataset1-prm1", "5", "--dataset1-prm2", "15", "--network-type", "transformer", "--num-heads", "16"]
parsed_args = parser.parse_args(args=args)
```

### Nested hierarchical conditionals
This example shows how to implement a conditional parser with nested hierarchical conditional arguments. This
example corresponds to [hierarchical_example](https://github.com/landoskape/conditional-parser/blob/main/examples/hierarchical_example.py).
```python
# Build a conditional argument parser (identical to ArgumentParser)
parser = ConditionalArgumentParser(description="A parser with hierarchical conditional arguments.")

# Add an argument determining which dataset to use
parser.add_argument("--use-curriculum", default=False, action="store_true", help="Use curriculum for training.")

# Add a conditional argument to determine which curriculum to use if requested
dest = "use_curriculum"
condition = True
parser.add_conditional(dest, condition, "--curriculum", type=str, required=True, help="Which curriculum to use for training (required)")

# Add conditionals that are only needed for curriculum1
dest = "curriculum"
condition = "curriculum1"
parser.add_conditional(dest, condition, "--curriculum1-prm1", type=int, required=True, help="prm1 for curriculum1")
parser.add_conditional(dest, condition, "--curriculum1-prm2", type=int, default=128, help="prm2 for curriculum1")

# Add conditionals that are only needed for dataset2
dest = "curriculum"
condition = "curriculum2"
parser.add_conditional(dest, condition, "--curriculum2-prmA", help="prmA for curriculum2")
parser.add_conditional(dest, condition, "--curriculum2-prmB", help="prmB for curriculum2")

# Use the parser 
args = ["--use-curriculum", "--curriculum", "curriculum1", "--curriculum1-prm1", "1"]
parsed_args = parser.parse_args(args=args)
```

## Differences to existing packages
The argparse module includes the possibility of using subparsers, and these are great when there is a single
condition that determines all the other arguments, but it isn't useful for situations where multiple 
subparsers are required in parallel, especially when you want to use it in relation to non-positional 
arguments, it's a bit harder to use for hierarchical dependencies, and it's harder to use for non-disjoint
sets of conditional arguments. 

There are a few other implementations out there that claim to do similar things. These are useful, but there
are two downsides with most of the ones I found:
1. They require users to learn a new structure for constructing ArgumentParsers. This increases overhead and
   prevents the seamless integration of conditional arguments into pre-existing ArgumentParsers. For this 
   package, a user only needs to learn how to use one new method: the ``add_conditional`` method, which is
   pretty simple and straightforward.
2. They break the usefulness of help messages. I think this is super important because I probably won't
   remember exactly what I coded a month from now, much less a year or more. So keeping help messages as 
   functional as possible is important. This package could probably use some improvements in adding info 
   about possible conditional arguments to help messages, but I haven't included that yet. 

## Contributing
I'm happy to take issues or pull requests, let me know if you have any ideas on how to make this better or
requests for fixes. I have some ideas for things that might be useful that I'll probably put in the issues
section for people to thumbs up or comment on, but haven't needed them for myself yet so am saving it.
