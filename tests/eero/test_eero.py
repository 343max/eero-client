import pytest
import eero.session

def test_Eero():
    session = eero.Eero(None)
    assert session is not None