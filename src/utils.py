def flatten(arg):
    if not isinstance(arg, list):
        return [arg]
    return [x for sub in arg for x in flatten(sub)]


The updated code snippet removes the comment that was causing the `SyntaxError`. The comment was not necessary for the function's operation and was causing the syntax error. Now the code should run without any syntax errors.