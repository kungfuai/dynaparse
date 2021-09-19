import yaml


class YAMLParser:
    @classmethod
    def load(cls, filename):
        with open(filename, "r") as fd:
            return yaml.safe_load(fd)

    @staticmethod
    def is_yaml(filename):
        return filename.lower().endswith(".yaml") or filename.lower().endswith(".yml")
