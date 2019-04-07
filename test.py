import time, json, sys
from collections import deque
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import requests

K = 4
BLOCK_LEN = 2
USER = "stephen"

def make_key(fname):
    with open(f'{fname}.pem', 'wb') as f:
        f.write(RSA.generate(2048).exportKey())

def load_key(fname):
    with open(f'{fname}.pem') as f:
        return RSA.importKey(f.read())

def str_byte(s): return s.encode("utf-8")

def sign(msg, sk): return sk.sign(str_byte(msg), "useless")

def verify(msg, sig, pk): return pk.verify(str_byte(msg), sig)

def hash(s): return SHA256.new(str_byte(str(s))).hexdigest()

def verify_work(block, k=K): return hash(block)[:k] == "0"*k

def verify_block(block, chain=None):

    if len(block.ledger) != BLOCK_LEN:
        raise InvalidBlockError("Ledger not the proper size")

    if chain is not None and block.prev_hash != hash(chain.curr if block.prev is None else block.prev):
        raise InvalidBlockError(f"Hash does not match previous hash")

    if not verify_work(block):
        raise InvalidBlockError(f"Invalid proof of work: expected prefix to be four zeros, got '{hash(block)[:K]}'")

    for vote in block.ledger:
        if not verify(vote.prefix, vote.sig, load_key(vote.person)):
            raise InvalidBlockError(f"Falsified signature for {vote.person} voting for {vote.vote}")

        if chain is not None:
            if vote.person in chain.seen:
                raise InvalidBlockError("Chain cannot contain the same vote twice!")
            chain.seen.add(vote.person)

    if len(set(vote.person for vote in block.ledger)) != len(block.ledger):
        raise InvalidBlockError("Block cannot contain the same vote twice!")

def str_vote(s):
    time, person, _, _, vote, _, sig = s.split()
    v = Vote(USER, "temp")
    v.time, v.person, v.vote, v.sig = float(time), person, vote, (int(sig),)
    v.prefix = f"{time} {person} voted for {vote}"
    return v

def str_block(s):
    l = list(filter(lambda x: len(x) > 0, (line for line in s.split("\n"))))
    hash = l[0].split(": ")[-1]
    b = Block(None, list(map(str_vote, l[1:-2])), l[-2].split(": ")[-1])
    b.prev_hash = hash if hash != "None" else None
    return b

def str_chain(s):
    blocks = [str_block(block) for block in s.split("-----BEGIN BLOCK-----") if block != ""]
    chain = Chain(blocks[0])
    for i in range(1, len(blocks)):
        chain.add_block(blocks[i])
    return chain

class InvalidBlockError(Exception):
    """ Raised when a block is invalid """

class Vote:

    def __init__(self, person, vote):
        self.person = person
        self.vote = vote
        self.time = time.time()
        self.prefix = f"{self.time} {person} voted for {vote}"
        self.sig = sign(self.prefix, load_key(person))

    def __str__(self): return f"{self.prefix} sig: {self.sig[0]}"

class Block:

    def __init__(self, prev=None, votes=[], proof=None):
        self.prev = None
        self.prev_hash = hash(prev) if prev is not None else "None"
        self.ledger = votes
        self.proof = proof

    def __str__(self):
        p = "-"*5
        header, footer =  f"{p}BEGIN BLOCK{p}\n", f"\n{p}END BLOCK{p}"
        return f"{header}previous hash: {self.prev_hash}\n" + '\n'.join(map(str, self.ledger)) + f"\nproof of work: {self.proof}{footer}"

    def mine(self):
        self.proof = 0
        while not verify_work(self):
            self.proof += 1

    def tally(self):
        counts = {}
        for vote in ledger:
            counts[vote.vote] = counts.get(vote.vote, 0) + 1
        return counts

class Chain:

    def __init__(self, curr=Block()):
        self.curr = curr
        self.seen = set()

    def __str__(self): return "\n\n".join(map(str, self.get_chain(self)))

    def get_chain(self, chain):
        l = deque([chain.curr])
        while l[0].prev is not None:
            l.appendleft(l[0].prev)
        return l

    def add_chain(self, chain):
        l = self.get_chain(chain)
        list(map(lambda x: verify_block(x, self), l))
        for vote in l[0].ledger:
            self.seen.remove(vote.person)
        self.add_block(l[0])
        self.curr = chain.curr

    def add_block(self, block):
        verify_block(block, self)
        block.prev = self.curr
        self.curr = block

    def tally(self):
        counts = {}
        for block in self.get_chain(self):
            for vote in block.ledger:
                counts[vote.vote] = counts.get(vote.vote, 0) + 1
        return counts

def get_data(): return json.loads(requests.get(f'{url}/get').text)

url = "http://127.0.0.1:5000"

def test():

    while True:
        try:
            prompt = input(">>> ")
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()

        prompt = prompt.split()
        cmd = prompt[0]

        if cmd == "get_chain":
            chain = str_chain(get_data()["chains"][int(prompt[1])])
            block = Block(chain.curr)
        elif cmd == "chain":
            print(chain)
        elif cmd == "push_chain":
            r = requests.get(f'{url}/vote', params={'chain':str(chain)})
        elif cmd == "add_block":
            chain.add_block(str_block(get_data()["blocks"][int(prompt[1])]))
        elif cmd == "add_vote":
            block.ledger.append(str_vote(get_data()["votes"][int(prompt[1])]))
        elif cmd == "vote":
            r = requests.get(f'{url}/vote', params={'vote_str':str(Vote(USER, prompt[1]))})
        elif cmd == "block":
            print(block)
        elif cmd == "push_block":
            r = requests.get(f'{url}/vote', params={'block':str(block)})
        elif cmd == "add_own_block":
            chain.add_block(block)
        elif cmd == "mine":
            block.mine()
        else:
            cmds = {"get": get_data, "tally": lambda: chain.tally(), "clear": lambda: requests.get(f'{url}/clear')}
            print(cmds[cmd]())

def setup_server():
    r = requests.get(f'{url}/vote', params={'vote_str':str(Vote("stephen", "trump"))})
    r = requests.get(f'{url}/vote', params={'vote_str':str(Vote("udbhav", "trump"))})
    r = requests.get(f'{url}/vote', params={'vote_str':str(Vote("luke", "clinton"))})
    r = requests.get(f'{url}/vote', params={'vote_str':str(Vote("andy", "clinton"))})
    r = requests.get(f'{url}/vote', params={'vote_str':str(Vote("justin", "trump"))})

    vote = Vote("luke", "clinton")
    vote.sig = (1273812738123,)
    r = requests.get(f'{url}/vote', params={'vote_str':str(vote)})

    chain = Chain(Block())
    b1 = Block(chain.curr, [Vote("stephen", "trump"), Vote("udbhav", "lenin")])
    b1.mine()
    print(hash(b1))
    chain.add_block(b1)

    r = requests.get(f'{url}/vote', params={'chain': chain})

if __name__ == "__main__":
    setup_server()

    #r = requests.get(f'{url}/vote', params={'vote_str':str(Vote("stephen", "trump"))})

    # chain = Chain(Block())
    # b1 = Block(chain.curr, [Vote("stephen", "trump"), Vote("udbhav", "lenin")])
    # b1.mine()
    # chain.add_block(b1)
    #
    # r = requests.get(f'{url}/vote', params={'chain': chain})

    #test()

    # b2 = Block(str(b1), [Vote("luke", "clinton")])
    # b2.mine()
    # chain.add_block(b2)
    #
    # #print(chain)
    #
    # # b4 = Block("hi test", [Vote("andy", "stalin")])
    # # b4.mine()
    # # chain.add_block(b4)
    #
    # b3 = Block(str(b2), [Vote("andy", "stalin")])
    # b3.mine()
    #
    # chain2 = Chain(b3)
    # b4 = Block(str(b3), [Vote("justin", "Caesar")])
    # b4.mine()
    # chain2.add_block(b4)
    #
    # chain.add_chain(chain2)
    #
    # print(chain)

    # b1 = Block()
    # b2 = Block(b1, [Vote("stephen", "trump"), Vote("udbhav", "lenin"), Vote("stephen", "hi")], 2932)
    #
    # print(b1)
    # print(b2)
    #
    # try:
    #     verify_block(b2)
    # except InvalidBlockError:
    #     print("can't use wrong PoW!")
    #     b2.mine()
    #
    # print(hash(b2))
    # verify_block(b2)
    #
    # vote = Vote("luke", "clinton")
    # vote.sig = (1273812738123,)
    #
    # b3 = Block(b2, [vote])
    # b3.mine()
    # print(b3)
    # verify_block(b3)

    # msg = "testing hi"
    # sk = load_key("stephen")
    # pk = sk.publickey()
    #
    # sig = sign(msg, sk)
    #
    # #print(sig)
    # print(verify(msg, sig, pk))
    # print(verify(msg, (2304234343,), pk))
    # print(verify(msg, sig, sk))
    # print(verify(msg, (2304234343,), sk))

    #print(SHA256.new(b"Nobody inspects the spammish repetition").hexdigest())
