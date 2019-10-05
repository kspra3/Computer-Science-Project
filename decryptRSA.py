from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto import Random
from base64 import b64encode, b64decode
from bitstring import BitArray
import math

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def decryptRSA():
    with open('ciphertext.txt', 'r') as cipherfile:
        extractedValue = cipherfile.read()
    with open('key.pem', mode='r') as keyfile:
        key = RSA.import_key(keyfile.read())
    pubkey = key

    newCipher = extractedValue
    chunks = math.ceil(len(newCipher) / 1376)
    message = ""

    for i in range(chunks):
        start = i*1376
        end = (i+1)*1376
        encrypted = bitstring_to_bytes(newCipher[start:end])
        #decodes the Base64 encoded bytes-like object or ASCII string s
        # returns the decoded bytes
        decrypted = decrypt(b64decode(encrypted), pubkey)
        message += decrypted.decode("ascii")


    with open('originMsg.txt','r') as orifile:
        msg1 = orifile.read()
        print('original msg: {}'.format(msg1))
        print('decrypted msg: {}'.format(message))
        print('original msg == decrypted msg: {}'.format(msg1 == message))

if __name__== "__main__":
    decryptRSA()