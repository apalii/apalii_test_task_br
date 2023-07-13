import logging
from urllib.parse import urljoin
from http import HTTPStatus as sc

import requests
import simplejson

LOGGER = logging.getLogger(__name__)


class BaseConfig:
    BASE_URL = "https://apis-sandbox.fedex.com"


class WebServiceResponseException(Exception):
    def __init__(self, code=sc.BAD_GATEWAY, description='Invalid response from the upstream server'):
        self.code = code
        self.description = description

class FedexAuthMixin:
    def authenticate(self):
        url = urljoin(BaseConfig.BASE_URL, "/oauth/token")
        payload = {
            "grant_type": "client_credentials",
            "client_id": "l7ecac81c1e42b46ec9eab51a7d8134e09",
            "client_secret": "baf2dbabe32a4a9aa8fb3eac42555329"
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.post(url, headers=headers, data=payload)
        return response.json()['access_token']


class FedexWebClient(FedexAuthMixin):
    SERVICE_NAME = "Fedex"

    def track(self, tracking_id="797806677146"):
        url = urljoin(BaseConfig.BASE_URL, "/track/v1/trackingnumbers")
        payload = {
            "includeDetailedScans": True,
            "trackingInfo": [
                {
                    "trackingNumberInfo": {
                        "trackingNumber": f"{tracking_id}",
                    }
                }
            ]
        }
        try:
            token = self.authenticate()
            headers = {
                'Content-Type': "application/json",
                'Authorization': f"Bearer {token}"
            }
            response = requests.post(url, data=simplejson.dumps(payload), headers=headers)
            status_code = response.status_code
            return response.json()
        except requests.exceptions.ConnectionError:
            LOGGER.info('Failed to connect to : {}'.format(url))
            raise WebServiceResponseException(description="Unable to connect to the {} service".format(
                self.SERVICE_NAME)
            )
        except requests.exceptions.JSONDecodeError:
            LOGGER.error('Receive unexpected response : {}'.format(response.text))
            raise WebServiceResponseException(code=status_code,
                                              description="Malformed response from {} service".format(self.SERVICE_NAME)
                                              )

