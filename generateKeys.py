from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA3_512
from Crypto import Random
from base64 import b64encode, b64decode
from bitstring import BitArray
import math

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