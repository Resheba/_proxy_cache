from src.core.response import BaseResponse


def test_base_response():
    response = BaseResponse()
    assert response.status == 'success'
    assert response.msg is None
    assert response.data is None


def test_base_response_model_dump():
    response = BaseResponse(status='error', msg='msg', data={'key': 'value'})
    assert response.model_dump(exclude_none=True) == {'status': 'error', 'msg': 'msg', 'data': {'key': 'value'}}
