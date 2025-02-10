
def url_join(*args):
    return "/".join(arg.strip("/") for arg in args)

# src/utils.py

from .filesystem import url_join

def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]