import threading
import pytest
from flask import Flask
import requests
import time
import random
import os
from io import BytesIO
from PIL import Image
from unittest.mock import Mock

import pytest

from counter.entrypoints.webapp import app, count_action, list_action  # Replace 'your_app_file_name' with the actual name of your Flask application file
import yaml 

def config(config_path="params.yaml"):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

configuration = config()
# Define the base URL for the Flask app
BASE_URL = configuration["BASE_URL"]  # Change the port if your app runs on a different port

# Start the Flask app in a separate thread for testing
def run_flask_app():
    app.run('127.0.0.1', port=5000, debug=False)

# Use pytest fixture to start and stop the Flask app
@pytest.fixture(scope='module')
def setup_teardown():
    # Start the Flask app in a separate thread
    thread = threading.Thread(target=run_flask_app)
    thread.daemon = True
    thread.start()

    # Wait for the app to start up
    time.sleep(1)

    yield

    # Tear down the Flask app after the tests
    requests.get(f"{BASE_URL}/shutdown")

    # Give some time for the app to shut down
    time.sleep(1)

def test_object_count_missing_file(setup_teardown):
    response = requests.post(f"{BASE_URL}/object-count", data={'threshold': '0.5'})
    assert response.status_code == 400
    assert response.json() == {'error': 'No file provided.'}

def test_object_count_invalid_threshold(setup_teardown):
    response = requests.post(f"{BASE_URL}/object-count", files={'file': open('resources/images/boy.jpg', 'rb')}, data={'threshold': 'invalid'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid threshold value. Please provide a float value between 0.0 and 1.0.'}

def test_object_count_large_file(setup_teardown):

    response = requests.post(f"{BASE_URL}/object-count", files={'file': open('resources/images/test.jpg', 'rb')}, data={'threshold': '0.5'})
    assert response.status_code == 400
    assert response.json() == {'error': 'File size exceeds the allowed limit.'}

def test_object_list_invalid_threshold(setup_teardown):
    response = requests.post(f"{BASE_URL}/object-list", files={'file': open('resources/images/boy.jpg', 'rb')}, data={'threshold': 'invalid'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid threshold value. Please provide a float value between 0.0 and 1.0.'}

def test_object_lits_large_file(setup_teardown):

    response = requests.post(f"{BASE_URL}/object-list", files={'file': open('resources/images/test.jpg', 'rb')}, data={'threshold': '0.5'})
    assert response.status_code == 400
    assert response.json() == {'error': 'File size exceeds the allowed limit.'}


if __name__ == "__main__":
    pytest.main(['-s', '-v', '--disable-pytest-warnings', '--color=yes', '--showlocals', '--maxfail=2', '--tb=short', '-k test_', '--timeout=600'])
