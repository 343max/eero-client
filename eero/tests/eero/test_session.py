from eero.session import SessionStorage

def test_session():
    ss = SessionStorage()
    assert ss.cookie is None
    assert ss is not None