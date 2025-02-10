from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_simple_urls(self):
    assert url_join("http://example.com", "page") == "http://example.com/page"

  def test_trims_trailing_slashes(self):
    assert url_join("http://example.com/", "page/") == "http://example.com/page"

  def test_handles_multiple_args(self):
    assert url_join("http://example.com", "page", "subpage") == "http://example.com/page/subpage"

  def test_trims_leading_slashes(self):
    assert url_join("/http://example.com", "page") == "http://example.com/page"

  def test_handles_no_scheme(self):
    assert url_join("example.com", "page") == "example.com/page"

  def test_handles_trailing_slash_on_last_arg(self):
    assert url_join("http://example.com", "page/") == "http://example.com/page"

  def test_handles_empty_args(self):
    assert url_join("http://example.com", "", "page") == "http://example.com/page"

  def test_handles_multiple_empty_args(self):
    assert url_join("http://example.com", "", "", "page") == "http://example.com/page"