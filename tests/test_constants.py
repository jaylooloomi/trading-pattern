from txf_mcp import constants as c


def test_timeframes_list():
    assert c.TIMEFRAMES == ["1s", "1min", "3min", "5min", "10min", "15min"]


def test_session_bounds():
    assert c.DAY_START == "08:45:00"
    assert c.DAY_END == "13:45:00"
    assert c.NIGHT_START == "15:00:00"
    assert c.NIGHT_END == "05:00:00"


def test_product_and_tz():
    assert c.PRODUCT == "TX"
    assert c.TZ == "+08:00"
