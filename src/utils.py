import os

def url_join(*args):
  parts = [str(arg).strip("/") for arg in args]
  return "/".join(parts)

class TestUrlJoin:
  def test_joins_paths(self):
    path = url_join("/api", "v1", "foo")
    assert path == "api/v1/foo"

  def test_joins_paths_when_some_have_leading_trailing_slash(self):
    path = url_join("/api/", "/v1/", "foo/")
    assert path == "api/v1/foo"

  def test_joins_a_full_uri(self):
    path = url_join("https://api.example.com/", "/v1", "foo")
    assert path == "https://api.example.com/v1/foo"

  def test_strips_bare_slashes(self):
    path = url_join("https://api.example.com/", "/", "/v1/", "/foo/", "/")
    assert path == "https://api.example.com/v1/foo"