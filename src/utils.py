from src.utils import url_join

def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]

def url_join_paths(*args):
    return url_join(*args)


In the rewritten code, I have replaced `sane_join` with `url_join` for URL construction as per the user's preference. I have also added a new function `url_join_paths` that uses `url_join` to join the provided paths. The `flatten` function remains the same as it is already clear and concise.