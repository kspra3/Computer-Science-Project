from Crypto.PublicKey import RSA
from Crypto import Random

def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    return key

def generateKeys():
    keysize = 1024
    key = newkeys(keysize)
    with open('key.pem', mode='wb') as keyfile:
        keyfile.write(key.export_key('PEM'))

if __name__== "__main__":
    generateKeys()