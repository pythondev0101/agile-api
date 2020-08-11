import pytest
import requests
import json
from requests.auth import HTTPBasicAuth

url = "http://127.0.0.1:5000"
headers = {"content-type": "application/json"}


def test_values_endpoints():
    r = requests.get(url + "/api/v1.0/values",auth=HTTPBasicAuth('admin', 'password'))
    result = r.json()
    assert r.status_code == 200
    assert len(result["values"]) == 4


def test_principles_endpoints():
    r = requests.get(url + "/api/v1.0/principles",auth=HTTPBasicAuth('admin', 'password'))
    result = r.json()
    assert r.status_code == 200
    assert len(result["principles"]) == 12


def test_create_delete_value():
    data = {"data": "Dummy data from pytest"}
    r = requests.post(url + "/api/v1.0/values", data=json.dumps(data), headers=headers,auth=HTTPBasicAuth('admin', 'password'))
    result = r.json()
    assert r.status_code == 200
    assert result == {"data": "Dummy data from pytest", "id": result["id"]}

    r = requests.delete(
        url + "/api/v1.0/values/{}".format(result["id"]), headers=headers,auth=HTTPBasicAuth('admin', 'password')
    )
    result = r.json()
    assert r.status_code == 200
    assert result["Result"] == True


def test_create_delete_principle():
    data = {"data": "Dummy data from pytest"}
    r = requests.post(
        url + "/api/v1.0/principles", data=json.dumps(data), headers=headers,auth=HTTPBasicAuth('admin', 'password')
    )
    result = r.json()
    assert r.status_code == 200
    assert result == {"data": "Dummy data from pytest", "id": result["id"]}

    r = requests.delete(
        url + "/api/v1.0/principles/{}".format(result["id"]), headers=headers,auth=HTTPBasicAuth('admin', 'password')
    )
    result = r.json()
    assert r.status_code == 200
    assert result["Result"] == True
