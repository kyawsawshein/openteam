from itertools import groupby


def encode(s: str) -> str:
    """
    Run‑length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """
    # TODO: implement
    # raise NotImplementedError("Implement me!")

    # raise NotImplementedError("Implement me!")
    # grouping the string like ("a", generator value) and then sum the gererator value
    return "".join(f"{char}{sum(1 for _ in grp)}" for char, grp in groupby(s))

# Solution : Using groupby to group the element with generator value and sum the value
