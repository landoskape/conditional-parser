import os, sys

mainPath = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.append(mainPath)

from conditional_parser import ConditionalArgumentParser


def main():
    # Build a conditional argument parser (identical to ArgumentParser)
    parser = ConditionalArgumentParser(
        description="A parser with parallel conditional arguments."
    )

    # Add an argument determining which dataset to use
    parser.add_argument(
        "dataset", type=str, help="Which dataset to use for training/testing."
    )

    # Add conditionals that are only needed for dataset1
    dest = "dataset"
    condition = "dataset1"
    parser.add_conditional(
        dest, condition, "--dataset1-prm1", default=1, type=int, help="prm1 for dataset1"
    )
    parser.add_conditional(
        dest, condition, "--dataset1-prm2", default=2, type=int, help="prm2 for dataset1"
    )

    # Add conditionals that are only needed for dataset2
    dest = "dataset"
    condition = "dataset2"
    parser.add_conditional(
        dest,
        condition,
        "--dataset2-prmA",
        default="A",
        type=str,
        help="prmA for dataset2",
    )
    parser.add_conditional(
        dest,
        condition,
        "--dataset2-prmB",
        default="B",
        type=str,
        help="prmB for dataset2",
    )

    # Add conditionals that are needed for both datasets 3 and 4, but not the other datasets
    dest = "dataset"
    condition = lambda dest: dest in ["dataset3", "dataset4"]
    parser.add_conditional(
        dest,
        condition,
        "--datasets34-prmX",
        default="X",
        type=str,
        help="prmX for datasets 3 and 4",
    )
    parser.add_conditional(
        dest,
        condition,
        "--datasets34-prmY",
        default="Y",
        type=str,
        help="prmY for datasets 3 and 4",
    )

    # Add an argument determining which kind of network to use
    parser.add_argument(
        "--network-type",
        type=str,
        default="mlp",
        help="Which type of network to use for training/testing.",
    )

    # Add conditionals that are only needed for mlps
    dest = "network_type"
    condition = "mlp"
    parser.add_conditional(
        dest,
        condition,
        "--mlp-layers",
        type=int,
        default=2,
        help="the number of mlp layers",
    )
    parser.add_conditional(
        dest,
        condition,
        "--mlp-layer-width",
        type=int,
        default=128,
        help="the width of each mlp layer",
    )

    # Add conditionals that are only needed for transfomers
    dest = "network_type"
    condition = "transformer"
    parser.add_conditional(
        dest,
        condition,
        "--num-heads",
        type=int,
        default=8,
        help="the number of heads to use in transfomer layers",
    )
    parser.add_conditional(
        dest,
        condition,
        "--kqv-bias",
        default=False,
        action="store_true",
        help="whether to use bias in the key/query/value matrices of the transfomer",
    )
    # ... etc.

    # Use the parser
    args = [
        "dataset1",
        "--dataset1-prm1",
        "5",
        "--dataset1-prm2",
        "15",
        "--network-type",
        "transformer",
        "--num-heads",
        "16",
    ]
    parsed_args = parser.parse_args(args=args)
    print("\n\nProvided args:", args)
    print("Returned namespace:", vars(parsed_args))

    # Use the parser for other arguments
    args = [
        "dataset3",
        "--datasets34-prmX",
        "hello",
        "--datasets34-prmY",
        "world",
        "--network-type",
        "mlp",
    ]
    parsed_args = parser.parse_args(args=args)
    print("\n\nProvided args:", args)
    print("Returned namespace:", vars(parsed_args))


if __name__ == "__main__":
    main()
