# Simple jokes API


## Description

Simple application, which provide API to operate with jokes.

Written in Python with Flask.

## Specification


## Run tests

```bash
git clone .. 
```

## Run application with Docker

First, install [docker-compose](https://docs.docker.com/compose/install/) if you doen's have it.

```bash
git clone...
cd ...
docker-compose up -d
# and check
curl 127.0.0.1:5000/api/healthcheck
{"message": "OK"}
```

### Note about Bearer auth
In Swagger UI use `Bearer xxx.yyy.zzz` as Authorization header.

You can get token `xxx.yyy.zzz` from `/auth` endpoint

## TODO

- Use mysql\postgres, create index on `user_id` in table `joke` for fast search user jokes
- check db and external api in `/healthcheck`
- Expose database and logs from container
- Use WSGI server
- Logic for revoke tokens, refresh tokens