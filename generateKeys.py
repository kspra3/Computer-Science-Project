"""
Program function: Generate RSA key pairs of 1024 bits and write into file.
"""

from Crypto.PublicKey import RSA
from Crypto import Random

def newkeys(keysize):
    """
    generates a RSA key given a key length

    parameters:
    keysize (int): number of bits in key

    return value:
    key: RSA key
    """
    # random number initialization
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    return key

def generateKeys(keyfile):
    """
    generates a new key rsa key and writes into a file

    parameters:
    keyfile (string): filename of file that the is key written to
    """
    keysize = 1024
    key = newkeys(keysize)
    with open(keyfile, mode='wb') as keyfile:
        keyfile.write(key.export_key('PEM'))
