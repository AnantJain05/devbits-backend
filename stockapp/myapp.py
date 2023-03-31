import requests
import json

URL1 = "http://127.0.0.1:8000/create_user/"
URL2 = "http://127.0.0.1:8000/userinfo/"


def get_data(id=None):
    data = {}
    if id is not None:
        data = {'id': id}

    headers = {'content-Type': 'application/json'}
    json_data = json.dumps(data)
    r = requests.get(url = URL2, headers = headers, data = json_data)
    data = r.json()
    print(data)

get_data(5)

def post_data():
    data = {
        'name': 'XYZ2',
        'email': 'xyz2@gmail.com',
        'password': '12345',
        'curamount': 1000000,
        'gain': 0,
        'loss': 0
    }

    headers = {'content-Type': 'application/json'}
    # if id is not None:
    #     data = {'id': id}
    json_data = json.dumps(data)
    r = requests.post(url = URL1, headers=headers, data = json_data)
    data = r.json()
    print(data)

# post_data()