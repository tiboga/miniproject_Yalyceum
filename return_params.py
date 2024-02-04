import json
def ret_params():
    with open('params.json', 'r') as f:
        data = json.load(f)
        return data
