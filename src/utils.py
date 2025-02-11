def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]


Based on the feedback, the issue is a circular import issue. The `url_join` function is not necessary for the `flatten` function, so it can be removed from the imports in `src/utils.py`. Here's the updated code:


def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]


This code removes the unnecessary import of `url_join` and should resolve the circular import issue, allowing the tests to pass.