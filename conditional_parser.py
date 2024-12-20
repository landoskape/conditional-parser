import sys
from typing import List, Any, Optional, Callable, Union
from copy import deepcopy
from inspect import signature
from argparse import ArgumentParser

__version__ = "0.0.2"


class ConditionalArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        """
        Initialize the ConditionalArgumentParser object.

        args and kwargs are passed directly to the ArgumentParser Object's initialization method.
        See standard ArgumentParser documentation for more information.
        """
        super(ConditionalArgumentParser, self).__init__(*args, **kwargs)
        self._conditional_parent = []
        self._conditional_condition = []
        self._conditional_args = []
        self._conditional_kwargs = []
        self._num_conditional = 0

    def parse_args(self, args: Optional[List[str]] = None, namespace=None):
        """Parse the arguments and return the namespace."""
        # if args not provided, use sys.argv
        if args is None:
            args = sys.argv[1:]

        # make a list of booleans to track which conditionals have been added
        already_added = [False for _ in range(self._num_conditional)]

        # prepare the conditionals in a dummy parser so the user can reuse self
        _parser = deepcopy(self)
        _parser = self._prepare_conditionals(_parser, args, already_added)

        # parse the arguments with the conditionals added in the dummy parser
        return ArgumentParser.parse_args(_parser, args=args, namespace=namespace)

    def add_conditional(self, dest, cond, *args, **kwargs) -> None:
        """
        add conditional argument that is only added when parent argument match a condition

        args:
            dest: is the destination of the parent (where to look in the namespace for conditional comparisons)
            cond: a variable or callable function that determines whether to add this conditional argument.
                  if callable, then it will be called on the value of dest
                  if not callable, then it will simply be compared to the value of dest, e.g. (dest==cond)
            *args: the arguments to add when the condition is met (via the standard add_argument method)
            **kwargs: the keyword arguments to add when the condition is met (via the standard add_argument method)
        """
        # attempt to add the conditional argument to a dummy parser to check for errors right away
        _dummy = deepcopy(self)
        _dummy.add_argument(*args, **kwargs)

        # if it passes, store the details to the conditional argument
        assert type(dest) == str, "dest must be a string corresponding to one of the destination attributes"
        self._conditional_parent.append(dest)
        self._conditional_condition.append(self._make_callable(cond))
        self._conditional_args.append(args)
        self._conditional_kwargs.append(kwargs)
        self._num_conditional += 1

    def _prepare_conditionals(self, _parser: ArgumentParser, args: List[str], already_added: List[bool]) -> ArgumentParser:
        """Prepare conditional arguments to the parser through a hierarchical parse."""
        # remove help arguments for an initial parse to determine if conditionals are needed
        args = [arg for arg in args if arg not in ["-h", "--help"]]
        namespace = ArgumentParser.parse_known_args(_parser, args=args)[0]

        # whenever conditionals aren't ready, add whatever is needed then try again
        if not self._conditionals_ready(namespace, already_added):
            # for each conditional, check if it is required and add it if it is
            for i, parent in enumerate(self._conditional_parent):
                if self._conditional_required(namespace, parent, already_added, i):
                    # add conditional argument
                    _parser.add_argument(*self._conditional_args[i], **self._conditional_kwargs[i])
                    already_added[i] = True

            # recursively call the function until all conditionals are added
            _parser = self._prepare_conditionals(_parser, args, already_added)

        # return a parser with all conditionals added
        return _parser

    def _make_callable(self, cond: Union[Callable, Any]) -> Callable:
        """make a function that returns a boolean from a function or value."""
        # if cond is callable, use it as is (assuming it takes in a single argument)
        if callable(cond):
            if len(signature(cond).parameters.values()) != 1:
                raise ValueError("If providing a callable for the condition, it must take 1 argument.")
            return cond

        # otherwise, create a function that compares the value to the provided value
        return lambda dest_value: dest_value == cond

    def _conditionals_ready(self, namespace, already_added) -> bool:
        """Check if all conditionals are finished."""
        # for each conditional, if it is required and not already added, return False
        for idx, parent in enumerate(self._conditional_parent):
            if self._conditional_required(namespace, parent, already_added, idx):
                return False

        # if all required conditionals are added, return True
        return True

    def _conditional_required(self, namespace, parent, already_added, idx) -> bool:
        """check if a conditional is required to be added"""
        # first check if the parent exists in the namespace
        if hasattr(namespace, parent):
            # then check if this conditional has already been added
            if not already_added[idx]:
                # if it hasn't been added and the conditional function matches the value in parent,
                # then return True to indicate that this conditional is required
                if self._conditional_condition[idx](getattr(namespace, parent)):
                    return True

        # otherwise return False to indicate that this conditional does not need to be added
        return False


# copy the docstring and signature from ArgumentParser for more useful help messages
ConditionalArgumentParser.__init__.__doc__ = ArgumentParser.__init__.__doc__
ConditionalArgumentParser.__init__.__signature__ = signature(ArgumentParser.__init__)
