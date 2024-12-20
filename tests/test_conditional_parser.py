import pytest
from conditional_parser import ConditionalArgumentParser
import sys


def test_basic_functionality():
    """Test that basic ArgumentParser functionality works."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--flag", action="store_true")
    parser.add_argument("--value", type=int, default=42)

    args = parser.parse_args(["--flag", "--value", "123"])
    assert args.flag is True
    assert args.value == 123

    args = parser.parse_args([])
    assert args.flag is False
    assert args.value == 42


def test_simple_conditional():
    """Test conditional argument with direct value matching."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_conditional("format", "csv", "--delimiter", default=",")

    # Test with CSV format
    args = parser.parse_args(["--format", "csv", "--delimiter", "|"])
    assert args.format == "csv"
    assert args.delimiter == "|"

    # Test with JSON format (delimiter should not be available)
    args = parser.parse_args(["--format", "json"])
    assert args.format == "json"
    assert not hasattr(args, "delimiter")

    # Test default CSV case
    args = parser.parse_args(["--format", "csv"])
    assert args.delimiter == ","


def test_callable_conditional():
    """Test conditional argument with callable condition."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--add_conditional", type=str, default="False")
    parser.add_conditional("add_conditional", lambda x: x.lower() == "true", "--extra-arg", action="store_true")

    # Test threshold above condition
    args = parser.parse_args(["--add_conditional", "True", "--extra-arg"])
    assert args.extra_arg

    # Test threshold below condition (should raise error if trying to use conditional)
    with pytest.raises(SystemExit):
        parser.parse_args(["--add_conditional", "False", "--extra-arg"])

    with pytest.raises(SystemExit):
        parser.parse_args(["--extra-arg"])


def test_hierarchical_conditionals():
    """Test nested conditional arguments."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--use-model", action="store_true")
    parser.add_conditional("use_model", True, "--model-type", choices=["cnn", "rnn"], required=True)
    parser.add_conditional("model_type", "cnn", "--kernel-size", type=int, default=3)
    parser.add_conditional("model_type", "rnn", "--hidden-size", type=int, default=128)

    # Test CNN path
    args = parser.parse_args(["--use-model", "--model-type", "cnn", "--kernel-size", "5"])
    assert args.use_model is True
    assert args.model_type == "cnn"
    assert args.kernel_size == 5

    args = parser.parse_args(["--use-model", "--model-type", "cnn"])
    assert args.kernel_size == 3
    assert not hasattr(args, "hidden_size")

    # Test RNN path (kernel-size should not be available)
    args = parser.parse_args(["--use-model", "--model-type", "rnn"])
    assert args.model_type == "rnn"
    assert args.hidden_size == 128
    assert not hasattr(args, "kernel_size")


def test_required_conditionals():
    """Test behavior of required conditional arguments."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--use-auth", action="store_true")
    parser.add_conditional("use_auth", True, "--username", required=True)

    # Should fail without required conditional
    with pytest.raises(SystemExit):
        parser.parse_args(["--use-auth"])

    # Should work with required conditional
    args = parser.parse_args(["--use-auth", "--username", "user123"])
    assert args.username == "user123"


def test_help_text():
    """Test that help text includes conditionals appropriately."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--mode", choices=["simple", "advanced"])
    parser.add_conditional("mode", "advanced", "--extra-param")

    # Capture help output
    old_stdout = sys.stdout
    help_output = []
    try:
        import io

        sys.stdout = io.StringIO()
        with pytest.raises(SystemExit):
            parser.parse_args(["--mode", "advanced", "--help"])
        help_output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    assert "--mode" in help_output
    assert "--extra-param" in help_output


def test_invalid_condition():
    """Test error handling for invalid conditions."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--value", type=int)

    # Test callable with wrong number of arguments
    with pytest.raises(ValueError):
        parser.add_conditional("value", lambda x, y: x > y, "--flag")


def test_sys_argv_default():
    """Test that the parser uses sys.argv when args=None."""
    parser = ConditionalArgumentParser()
    parser.add_argument("--test-flag", action="store_true")

    # Store original sys.argv
    original_argv = sys.argv

    try:
        # Modify sys.argv temporarily
        sys.argv = ["program_name", "--test-flag"]
        args = parser.parse_args()  # Note: not passing any args here
        assert args.test_flag is True

        # Test without flag
        sys.argv = ["program_name"]
        args = parser.parse_args()  # Note: not passing any args here
        assert args.test_flag is False
    finally:
        # Restore original sys.argv
        sys.argv = original_argv
