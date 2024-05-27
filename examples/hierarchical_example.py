import os, sys

mainPath = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.append(mainPath)

from conditional_parser import ConditionalArgumentParser


def main():
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
    parser.add_conditional(dest, condition, "--curriculum2-prmA", type=str, default="A", help="prmA for curriculum2")
    parser.add_conditional(dest, condition, "--curriculum2-prmB", type=str, default="B", help="prmB for curriculum2")

    # Use the parser
    args = ["--use-curriculum", "--curriculum", "curriculum1", "--curriculum1-prm1", "1"]
    parsed_args = parser.parse_args(args=args)
    print("\n\nProvided args:", args)
    print("Returned namespace:", vars(parsed_args))

    # Use the parser for a different curriculum
    args = ["--use-curriculum", "--curriculum", "curriculum2"]
    parsed_args = parser.parse_args(args=args)
    print("\n\nProvided args:", args)
    print("Returned namespace:", vars(parsed_args))

    # Use the parser for a curriculum without conditionals
    args = ["--use-curriculum", "--curriculum", "curriculum3"]
    parsed_args = parser.parse_args(args=args)
    print("\n\nProvided args:", args)
    print("Returned namespace:", vars(parsed_args))

    # Use the parser without a curriculum
    args = []
    parsed_args = parser.parse_args(args=args)
    print("\n\nProvided args:", args)
    print("Returned namespace:", vars(parsed_args))


if __name__ == "__main__":
    main()
