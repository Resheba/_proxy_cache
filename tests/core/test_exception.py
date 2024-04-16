from src.core.exception import BaseHTTPException


def test_base_exception_500():
    ex = BaseHTTPException(status_code=500, msg='msg', data={'key': 'value'})
    assert ex.status_code == 500
    assert ex.msg == 'msg'
    assert ex.data == {'key': 'value'}


def test_base_exception_400():
    ex = BaseHTTPException(status_code=400, msg='msg', data={'key': 'value'})
    assert ex.status_code == 400
    assert ex.msg == 'msg'
    assert ex.data == {'key': 'value'}
