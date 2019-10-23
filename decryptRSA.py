"""
Performs RSA decryption on ciphertext and compares decrypted plaintext against original plaintext.
Return 1 if original message matches decrypted plaintext, else returns 0.
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from Crypto import Random
from base64 import b64encode, b64decode
from bitstring import BitArray
import math

def decrypt(ciphertext, priv_key):
    """
    Decrypts a ciphertext using the given key

    parameters:
    ciphertext (bytes): ciphertext to be decrypted in bytes 
    priv_key (RSA key): key used to decrypt ciphertext

    return value:
    decrypted plaintext in bytes 
    """
    # creates a cipher object from the given key
    cipher = PKCS1_OAEP.new(priv_key)
    # decrypt ciphertext using cipher object
    return cipher.decrypt(ciphertext)

def bitstring_to_bytes(s):
    """
    Converts bitstring to bytes representation

    parameters:
    s (bitstring): bitstring to be converted into bytes

    return value:
    byte representation of bitstring
    """
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def decryptRSA(keyfile, ciphertextfile, originFilename):
    """
    Decrypts the ciphertext stored in ciphertextfile using the key stored in keyfile

    parameters:
    keyfile (string): name of file containing key
    ciphertextfile (string): name of file containing ciphertext
    originFilename (string): name of file containing original plaintext
    """
    # open ciphertextfile and read in ciphertext
    with open(ciphertextfile, 'r') as cipherfile:
        extractedValue = cipherfile.read()
    # open keyfile and read in key
    with open(keyfile, mode='r') as keyfile:
        key = RSA.import_key(keyfile.read())
    pubkey = key

    newCipher = extractedValue
    # ciphertext is too long, therefore split into chunks to decrypt
    # total number of chunks is computed
    chunks = math.ceil(len(newCipher) / 1376)
    # decrypted plaintext is stored into message
    decryptedMessage = ""

    # decrypt one chunk at a time
    for i in range(chunks):
        # chunk starting index
        start = i*1376
        # chunk ending index
        end = (i+1)*1376
        # Convert ciphertext from bitstring to bytes for decryption
        encrypted = bitstring_to_bytes(newCipher[start:end])
        #decrypts and decodes the Base64 encoded bytes object
        decrypted = decrypt(b64decode(encrypted), pubkey)
        # store decrypted plaintext into message
        decryptedMessage += decrypted.decode("ascii")

    outputArray = [None] * 3
    # open original message and compare with decrypted message
    with open(originFilename,'r') as orifile:
        originalMessage = orifile.read()
        # Store 1 into the first index of the outputArray if original message matches decrypted plaintext, else 0
        if originalMessage == decryptedMessage:
            outputArray[0] = 1
        else:
            outputArray[0] = 0

        # Store the original message into the second index of the outputArray
        outputArray[1] = str(originalMessage)
        # Store the decrypted message into the third index of the outputArray
        outputArray[2] = str(decryptedMessage)

        # Return the outputArray
        return outputArray
