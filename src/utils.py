from src.utils import url_join
from src.filesystem import sane_join

def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]

# No changes needed as the user prefers to use url_join for URL handling and the code doesn't use any URL handling functions.
# The user prefers to simplify path joining logic in code, but the code doesn't involve any path joining.
# If there was a path joining operation, it could be replaced with sane_join for consistency.