import jwt
from .conftest import TEST_SECRET

class TestAuthEndpoint():
    def test_good_credentials(self, client):
        res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        assert 'token' in res.json
        token = res.json['token']
        payload = jwt.decode(token, TEST_SECRET, algorithms=["HS256"])
        assert payload['user_login'] == "bob"
        assert res.status_code == 200

    def test_bad_password(self, client):
        res = client.post('/api/auth', json=dict(
            login='bob',
            password='incorrect_password'
        ))
        assert "User does not exist or password incorrect" in res.json['message']
        assert res.status_code == 400

    def test_bad_login(self, client):
        res = client.post('/api/auth', json=dict(
            login='baduser',
            password='badpassword'
        ))
        assert "User does not exist or password incorrect" in res.json['message']
        assert res.status_code == 400