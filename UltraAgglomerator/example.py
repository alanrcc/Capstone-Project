import requests
import json

# Constants
AI_URL = "http://0.0.0.0:5000/"
HEADER = {"Content-Type": "application/json"}

# Tests
def test1():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "nature" ]
    })

    resp = requests.post(url, headers=header, data=data)
    return json.loads(resp.text)

def test2():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "nature", "tree" ]
    })
    resp = requests.post(url, headers=header, data=data)
    return json.loads(resp.text)

def test3():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "nature", "flowers", "pure" ]
    })
    resp = requests.post(url, headers=header, data=data)
    return json.loads(resp.text)

def test_garbage():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "asdfafsca", "asdfasfnmfmrerjkjtkjjkkl", "opoooe" ]
    })
    resp = requests.post(url, headers=header, data=data)
    return json.loads(resp.text)

def test_special():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "dexamethasone" ]
    })

    resp = requests.post(url, headers=header, data=data)
    return json.loads(resp.text)

# Main
if __name__ == "__main__":
    extendedTest = False
    if extendedTest:
        print(test1())
        print(test2())
        print(test3())
        print(test_garbage())
    else:
        print(test_special())
