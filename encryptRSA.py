from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto import Random
from base64 import b64encode, b64decode
from bitstring import BitArray
import math

def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def hash(message):
    h_obj = SHA3_512.new()
    h_obj.update(message)
    return h_obj.hexdigest()

def encryptRSA(keyfile, outfile):
    #msg1 = str.encode(input("Enter input: "))
    #msg1.replace("|","")
    msg1 = str(input("Enter input: "))
    msg1 = msg1.replace("|", "")
    msg1 = str.encode(msg1)
    #print(msg1)
    chunks = math.ceil(len(msg1)/32)    

    # reading in key from keyfile
    with open(keyfile, mode='r') as keyfile:
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
    
    with open(outfile, "w+") as cipherfile:
        cipherfile.write(cipher)
    originFilename = 'origin_' + outfile
    with open(originFilename,'w+') as orifile:
        orifile.write(msg1.decode("ascii"))
    hashFilename = 'hash_' + outfile
    with open(hashFilename,'w+') as hashfile:
        hashfile.write(hash(msg1))

if __name__== "__main__":
    encryptRSA('key.pem', 'ciphertext.txt')
