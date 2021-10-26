import builtins


def read(t: builtins, name: str) -> int:
    try:
        value = t(input(name + ": "))
        return value
    except ValueError:
        print(f"field {name} must be {t.__name__}")
        raise ValueError(f"field {name} must be {t.__name__}")