import random
from flask import current_app
import requests


def get_vector_user(data):
    response_options = requests.options(current_app.config['URL_VECTOR_SERVER'])
    if response_options.status_code == 200:
        response_post = requests.post(current_app.config['URL_VECTOR_SERVER'], data=data)
        content = response_post.json()
        return content['vector']
    return mock_vector_server()


def mock_vector_server():
    return ','.join([str(random.random()) for _ in range(500)])