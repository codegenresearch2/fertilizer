def url_join(*parts):
    """
    Joins the provided URL parts into a single URL string.
    
    This function handles the joining of URL parts, ensuring that only one slash
    is used between the parts, and it trims any leading or trailing slashes from
    the parts before joining them.
    
    Args:
        *parts: Variable length argument list of URL parts to join.
    
    Returns:
        str: A single URL string formed by joining the provided parts.
    """
    from urllib.parse import urljoin
    
    # Normalize the parts by stripping leading and trailing slashes
    normalized_parts = [part.strip('/') for part in parts if part.strip('/')]
    
    # Join the parts using urljoin to ensure proper URL formation
    return urljoin('/', '/'.join(normalized_parts))