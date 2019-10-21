from Crypto.PublicKey import RSA
from Crypto import Random

def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    return key

def generateKeys(keyfile):
    keysize = 1024
    key = newkeys(keysize)
    with open(keyfile, mode='wb') as keyfile:
        keyfile.write(key.export_key('PEM'))

if __name__== "__main__":
    generateKeys('key.pem')