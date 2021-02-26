from dataclasses import dataclass, is_dataclass


def dataclass_nested(*args, **kwargs):
    """
    Decorator that can be a drop-in replacement for dataclass.
    Supports nesting.

    Reference: https://www.geeksforgeeks.org/creating-nested-dataclass-objects-in-python/
    """

    def wrapper(check_class):

        # passing class to investigate
        check_class = dataclass(check_class, **kwargs)
        o_init = check_class.__init__

        def __init__(self, *args, **kwargs):

            for name, value in kwargs.items():

                # getting field type
                ft = check_class.__annotations__.get(name, None)

                if is_dataclass(ft) and isinstance(value, dict):
                    obj = ft(**value)
                    kwargs[name] = obj
                try:
                    o_init(self, *args, **kwargs)
                except TypeError:
                    print("args:", args)
                    print("kwargs:", kwargs)
                    raise

        check_class.__init__ = __init__

        return check_class

    return wrapper(args[0]) if args else wrapper