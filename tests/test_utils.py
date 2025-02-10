from .helpers import SetupTeardown

from src.utils import url_join


class TestUrlJoin(SetupTeardown):
  def test_joins_urls(self):
    url = url_join("http://example.com", "test", "file")

    assert url == "http://example.com/test/file"

  def test_joins_urls_when_some_have_trailing_slash(self):
    url = url_join("http://example.com/", "/test", "file")

    assert url == "http://example.com/test/file"

  def test_joins_urls_with_empty_parts(self):
    url = url_join("http://example.com", "", "file")

    assert url == "http://example.com/file"

  def test_joins_urls_with_none_parts(self):
    url = url_join("http://example.com", None, "file")

    assert url == "http://example.com/file"