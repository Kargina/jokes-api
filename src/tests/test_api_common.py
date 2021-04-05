import pytest

class TestApiCommon():
    @pytest.mark.parametrize('endpoint', [
        "/api/user",
        "/api/auth"
    ])
    def test_send_unsupproted_json(self, client, endpoint):
        res = client.post(endpoint, json=dict(
            key='value'
        ))
        assert 'message' in res.json
        assert res.status_code == 400

    @pytest.mark.parametrize('endpoint', [
        "/api/user",
        "/api/auth",
        "/joke/1",
        "/jokes",
        "/joke/random"
    ])
    def test_method_not_allowed(self, client, endpoint):
        res = client.put('/api/user')
        assert 'message' in res.json
        assert res.status_code == 405

    def test_healthcheck(self, client):
        res = client.get('/api/healthcheck')
        assert res.json['message'] == "OK"
        assert res.status_code == 200

    def test_request_without_token(self, client):
        res = client.get('/api/jokes')
        assert 'Missing' in res.json['message']
        assert res.status_code == 400
