
from http.cookies import SimpleCookie

# function handle raw cookie
def parse_cookie(raw_data):
    res = []
    _cookie = SimpleCookie()
    _cookie.load(raw_data)
    _cookies = {k: v.value for k, v in _cookie.items()}

    for dict in _cookies:
        _res = {"name" : dict, "value" : _cookies[dict]}
        res.append(_res)

    return res