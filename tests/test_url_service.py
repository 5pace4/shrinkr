from shrinkr.services.url_service import base62_encode, make_shortend_url


def test_base62_encode_zero():
    assert base62_encode(0) == "0"


def test_base62_encode_known_value():
    assert base62_encode(61) == "z"
    assert base62_encode(62) == "10"


def test_make_shortend_url_is_deterministic():
    url = "https://example.com/some/page"
    assert make_shortend_url(url) == make_shortend_url(url)


def test_make_shortend_url_salt_changes_output():
    url = "https://example.com/some/page"
    assert make_shortend_url(url, salt=0) != make_shortend_url(url, salt=1)


def test_make_shortend_url_different_urls_differ():
    assert make_shortend_url("https://a.com") != make_shortend_url("https://b.com")
