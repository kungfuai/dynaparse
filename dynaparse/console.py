import sys
import warnings

from dynaparse.dynamic_configuration import DynamicConfiguration

HELP_STR = "usage: dynaparse init <filespec or importspec>\n"
HELP_STR += "\n"
HELP_STR += "Autogenerate dynaparse config and spec from either\n"
HELP_STR += "a filespec or importspec.\n"


warnings.filterwarnings("ignore")


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print(HELP_STR)
        exit(0)
    elif sys.argv[1] == "init" and len(sys.argv) == 3:
        sys.path.append("")
        dc = DynamicConfiguration(sys.argv[2])
        config_name = "_config_auto.json"
        spec_name = "_spec_auto.json"
        dc.save_config(config_name)
        dc.save_spec(spec_name)
        print(
            "Successfully wrote config to '%s' and spec to '%s'"
            % (config_name, spec_name)
        )
        exit(0)
    else:
        print(HELP_STR)
        raise Exception("Unable to parse command '%s'" % (" ".join(sys.argv)))
