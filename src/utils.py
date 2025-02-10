
def url_join(*args):
    return "/".join(arg.strip("/") for arg in args)

def flatten(arg):
  if not isinstance(arg, list):
    return [arg]
  return [x for sub in arg for x in flatten(sub)]


To address the circular import issue, I have moved the `url_join` function definition before the `flatten` function in the `src/utils.py` file. This ensures that `url_join` is fully initialized before it is used in the `flatten` function, thus avoiding the circular import error.