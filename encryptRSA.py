"""
Prompting of user for message to be encrypted.
Writes the ciphertext, hash and original message into output files.
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto import Random
from base64 import b64encode, b64decode
from bitstring import BitArray
import math

def encrypt(message, pub_key):
    """
    Encrypts a message using the given key

    parameters:
    message (bytes): message to be encrypted in bytes 
    pub_key (RSA key): key used to encrypt ciphertext

    return value:
    encrypted ciphertext in bytes 
    """
    # creates a cipher object from the given key
    cipher = PKCS1_OAEP.new(pub_key)
    # decrypt ciphertext using cipher object
    return cipher.encrypt(message)

def hash(message):
    """
    Computes hash of message using SHA3-512

    parameters:
    message (bytes): message to be hashed

    return value:
    the computed hash as a string
    """
    # create a SHA3_512 object for hashing
    h_obj = SHA3_512.new()
    # compute hash of message
    h_obj.update(message)
    # return computed hash as a string
    return h_obj.hexdigest()

def encryptRSA(keyfile, outfile):
    """
    Prompts the user for input.
    The input is then encrypted using RSA with key from keyfile and hashed with SHA3-512.
    The ciphertext and hash is written into text files.

    parameters:
    keyfile (string): name of file to read key from
    outfile (string): name of file to write ciphertext to
    """
    #msg1 = str.encode(input("Enter input: "))
    #msg1.replace("|","")

    # prompts user input for encryption
    msg1 = str(input("Enter input: "))
    # replace certain symbols
    msg1 = msg1.replace("|", "")
    # encode the message into bytes
    msg1 = str.encode(msg1)
    # message could be too long so split into chunks to encrypt
    # total number of chunks is computed
    chunks = math.ceil(len(msg1)/32)    

    # reading in key from keyfile
    with open(keyfile, mode='r') as keyfile:
        private = RSA.import_key(keyfile.read())

    # encrypted string is stored into cipher
    cipher = ""
        
    # encrypt one chunk at a time
    for i in range(chunks):
        # chunk starting index
        start = i*32
        # chunk ending index
        end = (i+1)*32
        # if last chunk, encrypt the rest of the message
        if i == chunks - 1:
            encrypted = b64encode(encrypt(msg1[start:], private))
        # if not the last chunk, only encrypt size of one chunk
        else:
            encrypted = b64encode(encrypt(msg1[start:end], private))
        # convert bytes to binary representation
        c = BitArray(encrypted)
        # store binary representation in cipher
        cipher += c.bin
    
    # write ciphertext into cipherfile
    with open(outfile, "w+") as cipherfile:
        cipherfile.write(cipher)
    # origin_ prefix for filename of original message
    originFilename = 'origin_' + outfile
    # write original message into orifile (for comparison during decryption)
    with open(originFilename,'w+') as orifile:
        orifile.write(msg1.decode("ascii"))
    # hash_ prefix for filename of hash
    hashFilename = 'hash_' + outfile
    # write computed hash into hashfile (for verifying authenticity of message)
    with open(hashFilename,'w+') as hashfile:
        hashfile.write(hash(msg1))

if __name__== "__main__":
    encryptRSA('key.pem', 'ciphertext.txt')
