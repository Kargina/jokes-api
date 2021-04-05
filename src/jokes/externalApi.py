import requests
from requests import RequestException


class ExternalApiException(Exception):
    pass


class ExternalJokesAPI:

    def get_joke(self):
        raise NotImplemented


class GeekJokesAPI(ExternalJokesAPI):

    _base_url = "https://geek-jokes.sameerkumar.website"

    @classmethod
    def get_joke(cls):
        try:
            result = requests.get(f"{cls._base_url}/api")
        except RequestException as e:
            raise ExternalApiException(f"Can't send request to external API: {e}")
        if result.status_code != 200:
            raise ExternalApiException(f"Response code from API is not 200: {result.status_code}, {result.text}")
        return result.text
