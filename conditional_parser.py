import sys
from typing import List, Any, Optional, Callable, Union
from copy import deepcopy
from inspect import signature
from argparse import ArgumentParser, Namespace

__version__ = "0.2.1"


class ConditionalArgumentParser(ArgumentParser):
    """An ArgumentParser that supports conditional arguments based on other argument values.

    This parser extends the standard ArgumentParser to allow adding arguments that only appear
    when certain conditions are met. This is useful for creating command-line interfaces where
    the value of one argument determines whether another argument is required.

    Example
    -------
    >>> parser = ConditionalArgumentParser()
    >>> parser.add_argument('--format', choices=['json', 'csv'], default='json')
    >>> parser.add_conditional('format', 'csv', '--delimiter',
    ...                       help='Delimiter for CSV output')
    >>> args = parser.parse_args(['--format', 'csv', '--delimiter', ','])
    >>> print(args.delimiter)
    ','
    """

    def __init__(self, *args, **kwargs):
        """Initialize the ConditionalArgumentParser.

        Parameters
        ----------
        *args : Any
            Positional arguments passed to ArgumentParser
        **kwargs : Any
            Keyword arguments passed to ArgumentParser

        Notes
        -----
        See the standard argparse.ArgumentParser documentation for details on
        available initialization parameters.
        """
        super(ConditionalArgumentParser, self).__init__(*args, **kwargs)
        self._conditional_parent = []
        self._conditional_condition = []
        self._conditional_message = []
        self._conditional_args = []
        self._conditional_kwargs = []
        self._num_conditional = 0

    def parse_args(
        self,
        args: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Namespace:
        """Parse command line arguments including conditional arguments.

        This method extends the standard ArgumentParser.parse_args() by first evaluating
        which conditional arguments need to be added based on the values of their parent
        arguments, then parsing all arguments together.

        Parameters
        ----------
        args : Optional[List[str]], default=None
            List of strings to parse. If None, default to sys.argv[1:].
        namespace : Optional[Namespace], default=None
            An object to store the parsed arguments. If None, a new Namespace object is
            created.

        Returns
        -------
        Namespace
            A namespace containing the parsed arguments.

        Examples
        --------
        >>> parser = ConditionalArgumentParser()
        >>> parser.add_argument('--format', choices=['json', 'csv'])
        >>> parser.add_conditional('format', 'csv', '--delimiter')
        >>> args = parser.parse_args(['--format', 'csv', '--delimiter', ','])
        >>> print(args.delimiter)
        ','
        """
        # if args not provided, use sys.argv
        if args is None:
            args = sys.argv[1:]

        _parser = deepcopy(self)

        if self.add_help and ("--help" in args or "-h" in args):
            # if the user is asking for help (and we're using the standard help system)
            # then we need to show all arguments including conditionals
            _parser = self._prepare_help(_parser)

        else:
            # make a list of booleans to track which conditionals have been added
            already_added = [False for _ in range(self._num_conditional)]

            # prepare the conditionals in a dummy parser so the user can reuse self
            _parser = self._prepare_conditionals(_parser, args, already_added)

        # parse the arguments with the conditionals added in the dummy parser
        return ArgumentParser.parse_args(_parser, args=args, namespace=namespace)

    def add_conditional(
        self,
        dest: str,
        cond: Union[Any, Callable],
        *args,
        **kwargs,
    ) -> None:
        """Add a conditional argument to the parser.

        This method adds an argument that is only included when the value of a parent
        argument matches a specified condition. The condition can be either a fixed value
        or a callable function that evaluates the parent argument's value.

        Parameters
        ----------
        dest : str
            The destination of the parent argument to compare.
        cond : Union[Any, Callable]
            A value or callable function that determines whether to add the conditional argument.
            If callable, it will be called on the value of dest. If not callable, it will be
            compared to the value of dest.
        *args : Any
            The arguments to add when the condition is met (via the standard add_argument method).
        **kwargs : Any
            The keyword arguments to add when the condition is met (via the standard add_argument method).

        Examples
        --------
        >>> parser = ConditionalArgumentParser()
        >>> parser.add_argument('--format', choices=['json', 'csv'])
        >>> parser.add_conditional('format', 'csv', '--delimiter',
        ...                       help='Delimiter for CSV output')
        >>> args = parser.parse_args(['--format', 'csv', '--delimiter', ','])
        >>> print(args.delimiter)
        ','
        """
        # attempt to add the conditional argument to a dummy parser to check for errors right away
        try:
            _dummy = deepcopy(self)
            _dummy.add_argument(*args, **kwargs)
        except Exception as e:
            raise ValueError(
                f"Conditional argument is incompatible with the parser. Error: {e}"
            )

        # if it passes, store the details to the conditional argument
        if not isinstance(dest, str):
            msg = (
                "dest must be a string corresponding to one of the destination attributes"
            )
            raise ValueError(msg)

        self._conditional_parent.append(dest)
        self._conditional_condition.append(self._make_callable(cond))
        self._conditional_message.append(self._callable_representation(dest, cond))
        self._conditional_args.append(args)
        self._conditional_kwargs.append(kwargs)
        self._num_conditional += 1

    def _prepare_conditionals(
        self,
        _parser: ArgumentParser,
        args: List[str],
        already_added: List[bool],
    ) -> ArgumentParser:
        """Recursively prepare and add conditional arguments to the parser.

        This method performs a hierarchical parse of the arguments, determining which
        conditional arguments should be added based on the values of their parent
        arguments. It continues recursively until all required conditional arguments
        have been added to the parser.

        Parameters
        ----------
        _parser : ArgumentParser
            The parser to which conditional arguments will be added.
        args : List[str]
            List of command line arguments to parse.
        already_added : List[bool]
            List tracking which conditional arguments have already been added.

        Returns
        -------
        ArgumentParser
            The parser with all required conditional arguments added.
        """
        # remove help arguments for an initial parse to determine if conditionals are needed
        args = [arg for arg in args if arg not in ["-h", "--help"]]
        namespace = ArgumentParser.parse_known_args(_parser, args=args)[0]

        # whenever conditionals aren't ready, add whatever is needed then try again
        if not self._conditionals_ready(namespace, already_added):
            # for each conditional, check if it is required and add it if it is
            for i, parent in enumerate(self._conditional_parent):
                if self._conditional_required(namespace, parent, already_added, i):
                    # add conditional argument
                    _parser.add_argument(
                        *self._conditional_args[i], **self._conditional_kwargs[i]
                    )
                    already_added[i] = True

            # recursively call the function until all conditionals are added
            _parser = self._prepare_conditionals(_parser, args, already_added)

        # return a parser with all conditionals added
        return _parser

    def _prepare_help(self, _parser: ArgumentParser) -> ArgumentParser:
        """Prepare the help parser to show all conditional arguments in the help output.

        This method adds all conditional arguments to the parser with modified help text
        that indicates when each argument is available. This ensures users can see all
        possible arguments when requesting help, even if some are conditional.

        Parameters
        ----------
        _parser : ArgumentParser
            The parser to which help text will be added.

        Returns
        -------
        ArgumentParser
            The parser with all conditional arguments and their help text added.

        Notes
        -----
        The help text for each conditional argument is modified to include information
        about when the argument becomes available, based on its parent argument's value.
        """
        zipped_conditionals = zip(
            self._conditional_message,
            self._conditional_args,
            self._conditional_kwargs,
        )
        for message, args, kwargs in zipped_conditionals:
            # Combine with existing help message
            existing_help = kwargs.get("help", "")
            if existing_help:
                kwargs["help"] = f"{existing_help} :: {message}"
            else:
                kwargs["help"] = message
            _parser.add_argument(*args, **kwargs)

        return _parser

    def _make_callable(self, cond: Union[Callable, Any]) -> Callable:
        """Convert a condition into a callable function.

        This method takes either a callable function or a value and returns a callable
        that can be used to evaluate whether a conditional argument should be added.

        Parameters
        ----------
        cond : Union[Callable, Any]
            Either a callable that takes one argument and returns a boolean, or
            a value that will be compared for equality with the parent argument's value.

        Returns
        -------
        Callable
            A function that takes one argument and returns a boolean.

        Raises
        ------
        ValueError
            If cond is callable but doesn't accept exactly one argument.

        Notes
        -----
        If cond is already callable, it must take exactly one argument.
        If cond is not callable, this method returns a function that compares
        its input to cond for equality.
        """
        # if cond is callable, use it as is (assuming it takes in a single argument)
        if callable(cond):
            if len(signature(cond).parameters.values()) != 1:
                raise ValueError(
                    "If providing a callable for the condition, it must take 1 argument."
                )
            return cond

        # otherwise, create a function that compares the value to the provided value
        return lambda dest_value: dest_value == cond

    def _callable_representation(self, parent: str, cond: Union[Callable, Any]) -> str:
        """Get a string representation of a callable object.

        This method takes a callable object and returns a string representation of it.
        If the callable is a lambda function, it returns the lambda definition.
        Otherwise, it returns the callable's name.
        """
        if callable(cond):
            if cond.__name__ != "<lambda>":
                message = f"(Available when {cond.__name__}({parent})=True)"
            else:
                message = f"(Available when lambda function condition on {parent} is met)"
        else:
            message = f"(Available when {parent}={cond})"
        return message

    def _conditionals_ready(
        self, namespace: Namespace, already_added: List[bool]
    ) -> bool:
        """Check if all required conditional arguments have been added to the parser.

        Parameters
        ----------
        namespace : Namespace
            The namespace containing the current parsed arguments.
        already_added : List[bool]
            List tracking which conditional arguments have already been added.

        Returns
        -------
        bool
            True if all required conditional arguments have been added,
            False otherwise.

        Notes
        -----
        This method checks each conditional argument to determine if:
        1. Its parent argument exists in the namespace
        2. The conditional hasn't been added yet
        3. The condition for adding it is met
        If any conditional meets all these criteria, it returns False to indicate
        more processing is needed.
        """
        # for each conditional, if it is required and not already added, return False
        for idx, parent in enumerate(self._conditional_parent):
            if self._conditional_required(namespace, parent, already_added, idx):
                return False

        # if all required conditionals are added, return True
        return True

    def _conditional_required(
        self,
        namespace: Namespace,
        parent: str,
        already_added: List[bool],
        idx: int,
    ) -> bool:
        """Check if a specific conditional argument needs to be added.

        Parameters
        ----------
        namespace : Namespace
            The namespace containing the current parsed arguments.
        parent : str
            The destination name of the parent argument.
        already_added : List[bool]
            List tracking which conditional arguments have already been added.
        idx : int
            Index of the conditional argument being checked.

        Returns
        -------
        bool
            True if the conditional argument needs to be added,
            False otherwise.

        Notes
        -----
        This method checks if:
        1. The parent argument exists in the namespace
        2. The conditional argument hasn't already been added
        3. The condition function evaluates to True for the parent's value
        """
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
