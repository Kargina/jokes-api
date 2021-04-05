from .conftest import BOB_JOKES

class TestJokeRandomEndpoint():
    def test_random_joke(self, client):
        token_res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        token = token_res.json['token']
        headers = {
            'Authorization': f'Bearer {token}',
        }

        joke_res = client.get('/api/joke/random', headers=headers)

        assert joke_res.json['id'] == len(BOB_JOKES) + 1
        assert joke_res.status_code == 200