# Simple jokes API


## Description

Simple application, which provides API to operate with jokes.

Written in Python with Flask.

## Specification
REST service provides:
- User registration
- User autharisation
- Joke creation for user
- Get all user jokes
- User joke update / delete
- Get random joke from external service
- Requests logging

## Run tests

```bash
git clone https://github.com/Kargina/jokes-api.git
cd jokes-api
python3 -m venv venv
./venv/bin/pip install -e .
./venv/bin/pytest
```

## Run application with Docker

First, install [docker-compose](https://docs.docker.com/compose/install/) if you doen's have it.

```bash
git clone https://github.com/Kargina/jokes-api.git
cd jokes-api
docker-compose up -d
# and check
curl 127.0.0.1:5000/api/healthcheck
{"message": "OK"}
```

## Swagger documentstion

Available via [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Note about Bearer auth
In Swagger UI use `Bearer xxx.yyy.zzz` as Authorization header.

You can get token `xxx.yyy.zzz` from `/auth` endpoint

## TODO

- Create index on `user_id` in table `joke` for fast search user jokes
- Check db and external api in `/healthcheck`
- Expose database and logs from container
- Use WSGI server
- Logic for revoke tokens, refresh tokens
- More tests
- Move secrets from code to env or some secure storage