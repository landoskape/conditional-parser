import os, sys

mainPath = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.append(mainPath)

from conditional_parser import ConditionalArgumentParser


def main(example):
    parser = ConditionalArgumentParser(description="A parser with conditional arguments.")
    parser.add_argument(
        "--use-regularization",
        default=False,
        action="store_true",
        help="Uses regularization if included.",
    )

    dest = "use_regularization"
    condition = True
    parser.add_conditional(
        dest,
        condition,
        "--regularizer-lambda",
        type=float,
        default=0.01,
        help="The lambda value for the regularizer.",
    )

    # Parse the arguments -- without the conditional
    if example == 0:
        args = []
        parsed_args = parser.parse_args(args=args)
        print("\nNo arguments:")
        print("Returned namespace:", vars(parsed_args))

    # Parse the arguments -- will add the conditional
    if example == 1:
        args = ["--use-regularization", "--regularizer-lambda", "0.1"]
        parsed_args = parser.parse_args(args=args)
        print("\nWith conditional arguments:")
        print("args:", args)
        print("Returned namespace:", vars(parsed_args))

    # Parse the arguments -- use conditional without the condition being met (will generate an error)
    if example == 2:
        print("\nAttempting to set conditional without it's parent condition being met:")
        args = ["--regularizer-lambda", "0.1"]
        print("args:", args)
        parsed_args = parser.parse_args(args=args)

    # Parse the arguments -- help message when conditional isn't met:
    if example == 3:
        print("\nHelp message (without conditional included):")
        args = ["--help"]
        print("args:", args)
        parsed_args = parser.parse_args(args=args)

    # Help will be printed and the program will exit, comment above for seeing the parser with the conditional included
    if example == 4:
        print("\nHelp message (including conditional):")
        args = ["--use-regularization", "--help"]
        print("args:", args)
        parsed_args = parser.parse_args(args=args)


if __name__ == "__main__":
    main(0)  # Conditional arguments not included
    main(1)  # With conditional arguments
    main(
        2
    )  # Conditional arguments set without being included (will generate an error, comment out to see example 3, 4)
    main(
        3
    )  # Help message without conditional (will end the program, comment out to see example 4)
    main(4)  # Help message with conditional
