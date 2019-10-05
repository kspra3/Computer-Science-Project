from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA3_512
from Crypto import Random
from base64 import b64encode, b64decode
from bitstring import BitArray
import math

def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def encryptRSA():
    msg1 = str.encode(input("Enter input: "))
    chunks = math.ceil(len(msg1)/32)    

    # reading in key from keyfile
    with open('key.pem', mode='r') as keyfile:
        private = RSA.import_key(keyfile.read())

    cipher = ""
        
    for i in range(chunks):
        start = i*32
        end = (i+1)*32
        # encodes the bytes-like object s
        # returns bytes
        if i == chunks - 1:
            encrypted = b64encode(encrypt(msg1[start:], private))
        else:
            encrypted = b64encode(encrypt(msg1[start:end], private))
        c = BitArray(encrypted)
        cipher += c.bin
    
    with open('ciphertext.txt', "w+") as cipherfile:
        cipherfile.write(cipher)
    with open('originMsg.txt','w+') as orifile:
        orifile.write(msg1.decode("ascii"))

if __name__== "__main__":
    encryptRSA()
