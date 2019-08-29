from typing import Any, Callable, Iterable, List, Tuple, TypeVar

T = TypeVar("T")
KEY = TypeVar("Key")


def group(
    iterable: Iterable[T], key: Callable[[T], Any]
) -> Iterable[Tuple[KEY, List[T]]]:
    groups = {}

    for item in iterable:
        if key(item) in groups:
            groups[key(item)].append(item)
        else:
            groups[key(item)] = [item]

    return groups.items()
