from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def make_key(fname):
    with open(f'{fname}.pem', 'wb') as f:
        f.write(RSA.generate(2048).exportKey())

def load_key(fname):
    with open(f'{fname}.pem') as f:
        return RSA.importKey(f.read())

def sign(msg, sk): return sk.sign(msg.encode("utf-8"), "useless")

def verify(msg, sig, pk): return pk.verify(msg.encode("utf-8"), sig)

msg = "testing hi"
sk = load_key("stephen")
pk = sk.publickey()

sig = sign(msg, sk)

#print(sig)
print(verify(msg, sig, k1))
print(verify(msg, (2304234343,), k1))
print(verify(msg, sig, k2))
print(verify(msg, (2304234343,), k2))

#print(SHA256.new(b"Nobody inspects the spammish repetition").hexdigest())
