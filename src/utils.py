def url_join(*args):
    """
    Joins the provided URL parts into a single URL string.
    
    This function handles the joining of URL parts, ensuring that only one slash
    is used between the parts, and it trims any leading or trailing slashes from
    the parts before joining them.
    
    Args:
        *args: Variable length argument list of URL parts to join.
    
    Returns:
        str: A single URL string formed by joining the provided parts.
    """
    # Convert each argument to a string
    parts = [str(arg) for arg in args]
    
    # Normalize the parts by stripping leading and trailing slashes
    normalized_parts = [part.strip('/') for part in parts]
    
    # Join the parts using a single slash
    return '/'.join(normalized_parts)