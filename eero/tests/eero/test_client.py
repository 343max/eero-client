from eero.client import Client
from eero.exception import ClientException
from nose.tools import raises
import responses
import json

@responses.activate
def test_client():
    c = Client()
    r = {
        'data': "some data",
        'meta': 
            {'code': 200}
    }
    responses.add(responses.GET, 'https://api-user.e2ro.com/2.2/helloworld', json=r)
    responses.add(responses.POST, 'https://api-user.e2ro.com/2.2/helloworld', json=r)
    assert "some data" == c.get('helloworld')
    assert "some data" == c.post('helloworld')    

@responses.activate
@raises(ClientException)
def test_client_error():
    c = Client()
    r = {
        'data': "unauthorized",
        'meta': 
            {'code': 403}
    }
    responses.add(responses.GET, 'https://api-user.e2ro.com/2.2/helloworld', json=r)
    c.get('helloworld')