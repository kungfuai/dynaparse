from argparse import ArgumentDefaultsHelpFormatter

from dynaparse import DynamicArgumentParser

from examples.config_composable import ExperimentConfig


class ExampleScriptArgumentParser(DynamicArgumentParser):
    """Example argument parser for a script."""

    def __init__(self):
        super().__init__(
            prog="example_script",
            description="Do stuff for example 1",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )

        self.add_argument(
            "--hard_coded_parameter",
            type=int,
            default=10,
            help="Help string for hard coded parameter",
        )


parser = ExampleScriptArgumentParser()
parser.append_config(ExperimentConfig())  # Added control to modify arguments
print("PARSED ARGUMENTS:")
print(parser.parse_args())
