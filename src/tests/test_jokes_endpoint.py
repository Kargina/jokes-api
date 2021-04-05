from .conftest import BOB_JOKES
import jwt
from .conftest import TEST_SECRET

class TestJokesEndpoint():

    def test_get_all_jokes(self, client):

        token_res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        token = token_res.json['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        joke_res = client.get('/api/jokes', headers=headers)
        assert len(joke_res.json) == len(BOB_JOKES)

    def test_post_joke(self, client):
        joke_text = 'New joke'
        token_res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        token = token_res.json['token']
        headers = {
            'Authorization': f'Bearer {token}',
        }

        joke_res = client.post('/api/jokes', headers=headers, json=dict(text= joke_text))
        assert joke_res.json['id'] == len(BOB_JOKES) + 1

    def test_post_joke_expired_token(self, client):
        joke_text = 'New joke'
        payload = {
          "iat": 1617570974,
          "nbf": 1617570974,
          "type": "access",
          "user_id": 12,
          "exp": 703893286, # 21.04.1992
        }
        expired_token = jwt.encode(payload, key=TEST_SECRET)
        headers = {
            'Authorization': f'Bearer {expired_token}',
        }
        joke_res = client.post('/api/jokes', headers=headers, json=dict(text=joke_text))
        assert joke_res.status_code == 401

    def test_post_joke_inkorrect_token(self, client):
        joke_text = 'New joke'
        headers = {
            'Authorization': f'Bearer qweqwe',
        }
        joke_res = client.post('/api/jokes', headers=headers, json=dict(text=joke_text))
        assert joke_res.status_code == 400