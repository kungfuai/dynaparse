# Table of Contents

1. [Overview](#overview)
2. [Type: int](#int-parameter-type)
3. [Type: float](#float-parameter-type)
4. [Type: bool](#boolean-parameter-type)
5. [Type: categorical](#categorical-parameter-type)
6. [Type: list](#list-parameter-type)
7. [Type: string](#string-parameter-type)

### Overview

Use this guide for creating your own spec files. A spec file is a list of key/value pair groupings in a json file, where each item in the list represents a parameter, and each key should be assigned using the guide below.

The contents will then be used to dynamically generate argparser objects.

### Int parameter type

|                  | Description                                        | Type | Required | Default   |
| ---------------- | -------------------------------------------------- | ---- | -------- | --------- |
| "parameter_type" | Parameter type selection (must be "int")           | str  | x        |           |
| "name"           | Name of parameter                                  | str  | x        |           |
| "help"           | Help string                                        | str  | x        |           |
| "required"       | Whether parameter is required                      | bool | x        |           |
| "default"        | Default value                                      | int  |          | None      |
| "distribution"   | Random distribution type (only supports "uniform") | str  |          | "uniform" |
| "p1"             | Low value for sampling                             | int  |          | None      |
| "p2"             | High value for sampling                            | int  |          | None      |

### Float parameter type

|                  | Description                                                    | Type  | Required | Default   |
| ---------------- | -------------------------------------------------------------- | ----- | -------- | --------- |
| "parameter_type" | Parameter type selection (must be "float")                     | str   | x        |           |
| "name"           | Name of parameter                                              | str   | x        |           |
| "help"           | Help string                                                    | str   | x        |           |
| "required"       | Whether parameter is required                                  | bool  | x        |           |
| "default"        | Default value                                                  | float |          | None      |
| "distribution"   | Random distribution type ("uniform" or "normal")               | str   |          | "uniform" |
| "p1"             | Low value for uniform sampling, mean for normal                | float |          | None      |
| "p2"             | High value for uniform sampling, standard deviation for normal | float |          | None      |

### Boolean parameter type

|                  | Description                                       | Type  | Required | Default |
| ---------------- | ------------------------------------------------- | ----- | -------- | ------- |
| "parameter_type" | Parameter type selection (must be "bool")         | str   | x        |         |
| "name"           | Name of parameter                                 | str   | x        |         |
| "help"           | Help string                                       | str   | x        |         |
| "required"       | Whether parameter is required                     | bool  | x        |         |
| "default"        | Default value                                     | bool  | x        |         |
| "is_constant"    | If True, do not change value with random sampling | float |          | True    |

### Categorical parameter type

|                  | Description                              | Type | Required | Default |
| ---------------- | ---------------------------------------- | ---- | -------- | ------- |
| "parameter_type" | Parameter type selection (must be "str") | str  | x        |         |
| "name"           | Name of parameter                        | str  | x        |         |
| "help"           | Help string                              | str  | x        |         |
| "required"       | Whether parameter is required            | bool | x        |         |
| "default"        | Default value                            | str  |          | None    |

### List parameter type

|                  | Description                                       | Type  | Required | Default |
| ---------------- | ------------------------------------------------- | ----- | -------- | ------- |
| "parameter_type" | Parameter type selection (must be "bool")         | str   | x        |         |
| "name"           | Name of parameter                                 | str   | x        |         |
| "help"           | Help string                                       | str   | x        |         |
| "required"       | Whether parameter is required                     | bool  | x        |         |
| "default"        | Default value                                     | bool  | x        |         |
| "is_constant"    | If True, do not change value with random sampling | float |          | True    |

### String parameter type

|                  | Description                              | Type | Required | Default |
| ---------------- | ---------------------------------------- | ---- | -------- | ------- |
| "parameter_type" | Parameter type selection (must be "str") | str  | x        |         |
| "name"           | Name of parameter                        | str  | x        |         |
| "help"           | Help string                              | str  | x        |         |
| "required"       | Whether parameter is required            | bool | x        |         |
| "default"        | Default value                            | str  |          | None    |
