import jwt
from .conftest import BOB_JOKE_ID, BOB_JOKES


class TestJokesIdEndpoint:

    def test_get_user_joke_by_id(self, client):

        token_res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        token = token_res.json['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        joke_res = client.get(f'/api/joke/{BOB_JOKE_ID}', headers=headers)
        assert joke_res.json['text'] in BOB_JOKES
        assert joke_res.status_code == 200

    def test_update_user_joke_by_id(self, client):
        token_res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        token = token_res.json['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        joke_text = 'Updated joke'
        joke_patch = client.patch(f'/api/joke/{BOB_JOKE_ID}', headers=headers, json=dict(text=joke_text))
        joke_get_updated = client.get(f'/api/joke/{BOB_JOKE_ID}', headers=headers)

        assert joke_get_updated.json['text'] == joke_text
        assert joke_patch.status_code == 200

    def test_delete_user_joke_by_id(self, client):
        token_res = client.post('/api/auth', json=dict(
            login='bob',
            password='password'
        ))
        token = token_res.json['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        joke_delete = client.delete(f'/api/joke/{BOB_JOKE_ID}', headers=headers)
        new_jokes_list = client.get(f'/api/joke/{BOB_JOKE_ID}', headers=headers)
        assert len(new_jokes_list.json) == len(BOB_JOKES) - 1
        assert joke_delete.status_code == 200
