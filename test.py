import time
from collections import deque
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

K = 2

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


chain = Chain(Block())
b1 = Block(chain.curr, [Vote("stephen", "trump"), Vote("udbhav", "lenin")])
b1.mine()
chain.add_block(b1)

b2 = Block(str(b1), [Vote("luke", "clinton")])
b2.mine()
chain.add_block(b2)

#print(chain)

# b4 = Block("hi test", [Vote("andy", "stalin")])
# b4.mine()
# chain.add_block(b4)

b3 = Block(str(b2), [Vote("andy", "stalin")])
b3.mine()

chain2 = Chain(b3)
b4 = Block(str(b3), [Vote("justin", "Caesar")])
b4.mine()
chain2.add_block(b4)

chain.add_chain(chain2)

print(chain)

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
