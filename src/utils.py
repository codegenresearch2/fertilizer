def join_urls(*args):
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
    # Normalize the parts by stripping leading and trailing slashes
    normalized_parts = [str(arg).strip('/') for arg in args]
    
    # Join the normalized parts using a single slash
    return '/'.join(normalized_parts)