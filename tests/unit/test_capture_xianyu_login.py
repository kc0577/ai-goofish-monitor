from scripts.capture_xianyu_login import has_account_cookie, is_login_url


def test_detects_known_account_cookie_without_exposing_values():
    cookies = [{"name": "anonymous", "value": "x"}, {"name": "unb", "value": "secret"}]
    assert has_account_cookie(cookies) is True


def test_rejects_anonymous_cookie_set():
    assert has_account_cookie([{"name": "cna", "value": "anonymous"}]) is False


def test_identifies_login_redirects():
    assert is_login_url("https://passport.goofish.com/mini_login.htm") is True
    assert is_login_url("https://www.goofish.com/") is False
