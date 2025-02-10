
def url_join(*args):
    parts = [arg.strip("/") for arg in args]
    return "/".join(parts)


# src/utils.py

from .filesystem import url_join

def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]