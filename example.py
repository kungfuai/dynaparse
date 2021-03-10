from argparse import ArgumentDefaultsHelpFormatter

from dynaparse import DynamicArgumentParser


class Example1ArgumentParser(DynamicArgumentParser):
    """Example number 1 argument parser."""

    def __init__(self):
        super().__init__(
            prog="example1",
            description="Do stuff for example 1",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )

        self.add_argument(
            "--param1", type=int, default=10, help="My help, super cool, wow, neat-o"
        )


parser = Example1ArgumentParser()
print("PARSED ARGUMENTS:")
print(parser.parse_args())