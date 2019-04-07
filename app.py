from flask import request, Flask
import json

app = Flask(__name__)

data = {"votes": [], "chains": [], "blocks": []}

def load_json():
    with open("data.json") as f:
        return json.load(f)

def dump_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f)
    return json.dumps(data)

@app.route("/")
def main():
    return "Hello this is voting"

@app.route('/vote')
def vote():
    if 'vote_str' in request.args:
        data["votes"].append(request.args.get('vote_str'))
    if 'chain' in request.args:
        data["chains"].append(request.args.get('chain'))
    if 'block' in request.args:
        data["blocks"].append(request.args.get('block'))

    dump_json(data)
    return "done"

@app.route('/get')
def get():
    data = load_json()
    return dump_json(data)

@app.route('/clear')
def clear():
    global data
    data = {"votes": [], "chains": [], "blocks": []}
    dump_json(data)
    return "wiped"
