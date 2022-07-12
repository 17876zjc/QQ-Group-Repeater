import json
import requests

url = "https://majsoul.paulzzh.com/api/v2/record"

def recordpaipu(paipu):
    data = {'uuid':str(paipu)}
    print(data)
    r = requests.post(url,params=data)
    res = r.json()
    return res