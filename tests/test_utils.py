from src.utils import url_join

def url_join(*args):
    base_url = ''
    paths = []
    for arg in args:
        if arg.startswith('http://') or arg.startswith('https://'):
            base_url = arg.rstrip('/')
        else:
            paths.append(arg.strip('/'))
    return base_url + '/' + '/'.join(paths)

# Test cases
assert url_join('http://example.com', 'path', 'file') == 'http://example.com/path/file'
assert url_join('http://example.com', '/path', 'file') == 'http://example.com/path/file'
assert url_join('http://example.com/', 'https://another.com/path') == 'https://another.com/path'
assert url_join('http://example.com/', '/') == 'http://example.com'
assert url_join('http://example.com', '', 'file') == 'http://example.com/file'
assert url_join('http://example.com/', 'path/') == 'http://example.com/path'
assert url_join('http://example.com/', '/path/') == 'http://example.com/path'
assert url_join('http://example.com/', 'https://another.com/path') == 'https://another.com/path'