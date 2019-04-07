from flask import request, Flask
from test import *
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
    global data
    data = load_json()
    return dump_json(data)

@app.route('/clear')
def clear():
    global data
    data = {"votes": [], "chains": [], "blocks": []}
    dump_json(data)
    return "wiped"

@app.route('/set_chain/<int:id>')
def set_chain(id):
    global chain, block
    chain = str_chain(data["chains"][id])
    block = Block(chain.curr)
    return "done"

@app.route('/get_chain')
def get_chain():
    return str(chain)

@app.route('/push_chain')
def push_chain():
    data["chains"].append(str(chain))
    return dump_json(data)

@app.route('/add_block/<int:id>')
def add_block(id):
    chain.add_block(str_block(data["blocks"][id]))
    return "done"

@app.route('/add_vote/<int:id>')
def add_vote(id):
    block.ledger.append(str_vote(data["votes"][id]))
    return "done"

@app.route('/push_block')
def push_block():
    data["blocks"].append(str(block))
    return dump_json(data)

@app.route('/mine')
def mine():
    block.mine()
    return "done"

@app.route('/get_block')
def get_block():
    return str(block)

@app.route('/add_own_block')
def add_own_block():
    chain.add_block(block)
    return "done"

@app.route('/tally')
def tally():
    return json.dumps(chain.tally())
