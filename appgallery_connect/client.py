import os
import json
from requests import Session

REQUIRED_CONFIG_KEYS = [
    'client_id',
    'client_secret',
    'application_id',
]

API_URL = 'https://connect-api.cloud.huawei.com/api'
API_VERSION = 'v1'


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}

    for filename in os.listdir(get_abs_path('schemas')):
        path = os.path.join(get_abs_path('schemas'), filename)

        file_raw = str(filename).replace('.json', '')

        with open(path) as file:
            schemas[file_raw] = json.load(file)

    return schemas


class Client:
    def __init__(self, config_path: str):
        self._req_session = Session()
        self._req_session.headers.update({
            'Content-Type': 'application/json'
        })

        self._config = self._get_config(config_path)
        self._token = self._get_token()

    @staticmethod
    def _get_config(config_path: str):
        # TODO: Check REQUIRED_CONFIG_KEYS
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.loads(config_file.read())

        return config

    def _get_token(self):
        urn = f'oauth2/{API_VERSION}/token'
        uri = '/'.join([API_URL, urn])

        payload = json.dumps({
            'grant_type': 'client_credentials',
            'client_id': self._config['client_id'],
            'client_secret': self._config['client_secret']
        })

        response = self._req_session.post(url=uri, data=payload)

        if response.status_code == 200:
            access_token = response.json()['access_token']

            self._req_session.headers.update({
                'Authorization': f'Bearer {access_token}',
                'client_id': self._config['client_id']
            })

            return access_token
        else:
            # TODO:
            pass

    def installations_export(self, response_format: str = 'raw', **kwargs):
        urn = f'report/distribution-operation-quality/{API_VERSION}/appDownloadExport/{self._config["application_id"]}'
        uri = '/'.join([API_URL, urn])

        params = kwargs

        response = self._req_session.get(url=uri, params=params)

        if response.status_code == 200:
            data = response.json()

            if data.get('ret', {}).get('code', None) == 0:
                if response_format == 'raw':
                    data.pop('ret')
                    return data
                else:
                    # TODO: Other formats (csv, json)
                    pass
            else:
                # TODO:
                pass
        else:
            # TODO: Code with expired token
            pass
