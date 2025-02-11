from src.utils import url_join

def url_join(*args):
  for arg in args:
    if arg.startswith('http://') or arg.startswith('https://'):
      return arg
  return "/".join([str(arg).strip("/") for arg in args if str(arg).strip("/")])

# Test cases
assert url_join('http://example.com', 'path', 'file') == 'http://example.com/path/file'
assert url_join('http://example.com', '/path', 'file') == 'http://example.com/path/file'
assert url_join('http://example.com/', 'https://another.com/path') == 'https://another.com/path'
assert url_join('http://example.com/', '/') == 'http://example.com'
assert url_join('http://example.com', '', 'file') == 'http://example.com/file'
assert url_join('http://example.com/', 'path/') == 'http://example.com/path'
assert url_join('http://example.com/', '/path/') == 'http://example.com/path'
assert url_join('http://example.com/', 'https://another.com/path') == 'https://another.com/path'