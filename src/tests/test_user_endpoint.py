from jokes.config import USER_MAX_LEN

class TestUserEndpoint():
    # user_endpoint = '/api/user'

    def test_create_new_user(self, client):
        res = client.post('/api/user', json=dict(
            login='test_login',
            password='test_login'
        ))

        assert "id" in res.json
        assert res.status_code == 201

    def test_create_user_twice(self, client):
        client.post('/api/user', json=dict(
            login='test_login',
            password='test_login'
        ))
        res = client.post('/api/user', json=dict(
            login='test_login',
            password='test_login'
        ))
        assert "Login already exist" in res.json['message']
        assert res.status_code == 400

    def test_login_over_max_length(self, client):
        res = client.post('/api/user', json=dict(
            login='a' * (USER_MAX_LEN + 1),
            password='test_login'
        ))

        assert str(USER_MAX_LEN) in res.json['message']
        assert res.status_code == 400

    def test_login_max_length(self, client):
        res = client.post('/api/user', json=dict(
            login='a' * (USER_MAX_LEN),
            password='test_login'
        ))
        assert 'id' in res.json
        assert res.status_code == 201