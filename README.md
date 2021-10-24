# dynaparse

Enable dynamic configuration of scripts, especially for machine learning applications. In most cases, the "core pipeline" is a training pipeline and the "modular components" are ML models.

<p align="center">
  <img src="./docs/img/dynaparse-diagram.png" width=400 />
</p>

**Note: `dynaparse` is in alpha release for initial testing and is not guaranteed stable.**

# Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Terminology](#terminology)
4. [Quickstart](#quickstart)
5. [Spec reference](#spec-reference)
6. [Crash course](#crash-course)

# Requirements

- Python 3.6+

# Installation

```
pip install dynaparse
```

# Terminology

- `config` - A (potentially nested) structure containing key/value pairs with type enforcement. Example:

```
# config.json
{
  "backbone": "resnet50",
  "num_classes": 4,
  ...
}
```

- `spec` - A (potentially nested) structure with metadata about parameters in a config (same function as an `argparse` argument). Example:

```
# spec.json
{
    "name": "backbone",
    "help": "Selection of object detection backbone",
    "required": true,
    "default": "resnet18",
    "parameter_type": "categorical",
    "options": ["resnet18", "resnet50", "resnet101"]
},
{
    "name": "num_classes",
    "help": "Number of target classes",
    "required": true,
    "default": 1,
    "parameter_type": "int"
},
...
```

**Don't want to take the time to create a spec?** No problem! Use the CLI: `dynaparse init config[.json/.yaml]` will generate one for you (verbosely).

When using `dynaparse`, loading a config with a spec will validate types as well as options for categorical parameters.

# Quickstart

To get started, simply inherit `DynamicArgumentParser` instead of `ArgumentParser` in your script's argument parser.

```
# script.py
from argparse import ArgumentDefaultsHelpFormatter
#from argparse import ArgumentParser  # Dont do this
from dynaparse import DynamicArgumentParser # Do this instead

class TrainingSessionArgumentParser(DynamicArgumentParser):
    """Example argument parser for a script."""
    def __init__(self):
        super().__init__(
            prog="training_session",
            description="Train a machine learning model",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )

        self.add_argument(
            "--learning_rate",
            type=float,
            default=1e-4,
            help="",
        )

if __name__ == "__main__":
    parser = TrainingSessionArgumentParser()
    args = parser.parse_args()
    # ... do something with args
```

Your script can now be run with any `config` or `spec` (neither are required). The `args` object is returned as usual, but with dynamic values. Run `python script.py --help` for details:

```
usage: training_session [-h] [--spec SPEC] [--config CONFIG] [--random_sample] [--learning_rate LEARNING_RATE]

Train a machine learning model

optional arguments:
  -h, --help            show this help message and exit
  --spec SPEC           Dynamic configuration spec file specifying metadata for dynamic named arguments. Loads default values
                        unless config file overrides. (default: None)
  --config CONFIG       File specifying values following the schema in 'spec'. Command line args will override these values.
                        (default: None)
  --random_sample       If True, generate random parameters from the specified dynamic configuration. (default: False)
  --learning_rate LEARNING_RATE

NOTE: This script uses a dynamic argument parser for configuration.
See https://github.com/kungfuai/dynaparse for more information.
```

Complete the crash course below for more details.

# Spec reference

When creating your own spec files, reference the [README](./dynaparse/parameters/README.md) in `./dynaparse/parameters`.

# Crash course

Clone this repo and complete the below steps in sequence.

As in `examples/script.py`, inheriting `dynaparse.DynamicArgumentParser` enables the dynamic functionality. Take a look at this basic script to get an idea of how to get started.

Next, follow these steps to get familiar with the workflow:

1. `dynaparse init examples/config_example.json`
2. Edit `_spec_auto.json`:

- Change the categorical parameter's `parameter_type` from `str` to `categorical`
- Add another key in this parameter's dict: `"options": ["option1", "option2", "option3"]`

3. `python -m examples.script --help` (notice the three special arguments added)
4. `python -m examples.script --spec _spec_auto.json --help`
5. `python -m examples.script --spec _spec_auto.json`

- Notice that programmatically, you can access these parsed args with dot notation, e.g. `nested_section.int_parameter_1`

6. Change some values in `_config_auto.json`
7. `python -m examples.script --spec _spec_auto.json --config _config_auto.json`
8. `python -m examples.script --spec _spec_auto.json --nested_section.int_parameter_1 999`
9. `python -m examples.script --spec _spec_auto.json --categorical_parameter_1 option1`
10. `python -m examples.script --spec _spec_auto.json --categorical_parameter_1 option4`

- This should throw an error, as expected (`option4` not in the options list we added previously)
