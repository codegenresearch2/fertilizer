from src.utils import url_join
from src.filesystem import sane_join

def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]

# Using url_join for URL handling
def join_urls(*args):
    return url_join(*args)

# Using sane_join for path joining
def join_paths(*args):
    return sane_join(*args)