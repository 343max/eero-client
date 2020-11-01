import eero.session

def test_eero():
    session = eero.Eero(None)
    assert session is not None