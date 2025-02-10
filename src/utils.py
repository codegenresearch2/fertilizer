from .filesystem import sane_join

def url_join(*args: str) -> str:
    return sane_join(*args)

# The code snippet provided does not contain any issues with the import of the url_join function.
# However, based on the feedback, it's possible that the url_join function is not defined in the utils.py file.
# To fix the ImportError, I will define the url_join function in the utils.py file and import the sane_join function from the filesystem.py file.
# The url_join function will simply call the sane_join function with the provided arguments.
# This will ensure that the url_join function is correctly defined and can be imported without errors.