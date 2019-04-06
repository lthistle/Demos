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

class InvalidBlockError(Exception):
    """ Raised when a block is invalid """

    # def __init__(self, expression, message):
    #     self.expression = expression
    #     self.message = message
    #
    # def  __str__(self): return f"{self.expression}{self.message}"

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
        self.prev = prev
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

    def send(self):
        if not verify_work(self):
            raise InvalidBlockError(f"Invalid proof of work: expected prefix to be four zeros, got '{hash(self)[:K]}'")

        for vote in self.ledger:
            if not verify(vote.prefix, vote.sig, load_key(vote.person)):
                raise InvalidBlockError(f"Falsified signature for {vote.person} voting for {vote.vote}")

        # TODO: propagate block to server

class Chain:

    def __init__(self, curr=None):
        self.curr = curr

    def __str__(self): return "\n\n".join(map(str, self.get_chain(self)))

    def get_chain(self, chain):
        l = deque([chain.curr])
        while l[0].prev is not None:
            l.appendleft(l[0].prev)
        return l

    # def add_chain(self, chain):
    #     self.get_chain(chain)[0].prev = self.curr
    #     return chain

    def add_block(self, votes):
        block = Block(self.curr, votes)
        block.mine()
        self.curr = block


b1 = Block()
b2 = Block(b1, [Vote("stephen", "trump"), Vote("udbhav", "lenin")])
b2.mine()

# b3 = Block(b2, [Vote("luke", "clinton")])
# b3.mine()

chain = Chain(b2) 
chain.add_block([Vote("luke", "clinton")])
print(chain)

# b1 = Block()
# b2 = Block(b1, [Vote("stephen", "trump"), Vote("udbhav", "lenin")], 2932)
#
# print(b1)
# print(b2)
#
# try:
#     b2.send()
# except InvalidBlockError:
#     print("can't use wrong PoW!")
#     b2.mine()
#
# print(hash(b2))
# b2.send()
#
# vote = Vote("luke", "clinton")
# vote.sig = (1273812738123,)
#
# b3 = Block(b2, [vote])
# b3.mine()
# print(b3)
# b3.send()

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
