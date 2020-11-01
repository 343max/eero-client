from eero.exception import ClientException

def test_exception():
    e = ClientException("status", "error_message")
    assert "status" == e.status
    assert "error_message" == e.error_message