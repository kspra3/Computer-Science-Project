"""
Verifies the authenticity of a ciphertext by decrypting the ciphertext,
computing its hash and comparing the computed hash against the received hash.
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from bitstring import BitArray
from base64 import b64encode, b64decode
import math

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

def verify(keyfile, ciphertextfile):
    """
    Decrypts the ciphertext stored in ciphertextfile using key from keyfile.
    Then, computes the hash of plaintext and compare computed hash against received hash.
    Outputs whether the computed hash matches received hash.

    parameters:
    keyfile (string): name of file containing key
    ciphertextfile (string): name of file containing ciphertext
    """
    # reads the ciphertext from ciphertextfile
    with open(ciphertextfile, 'r') as cipherfile:
        extractedValue = cipherfile.read()
    # reads the key from keyfile
    with open(keyfile, mode='r') as keyfile:
        key = RSA.import_key(keyfile.read())
    pubkey = key

    newCipher = extractedValue
    # ciphertext is too long, therefore split into chunks to decrypt
    # total number of chunks is computed
    chunks = math.ceil(len(newCipher) / 1376)
    # decrypted plaintext is stored into message
    message = ""

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
        message += decrypted.decode("ascii")

    hashFilename = "hash_" + ciphertextfile
    # store received hash from hashfilename into hashMsg
    with open(hashFilename,'r') as hashfile:
        hashMsg = hashfile.read()
    # computes the hash of the decrypted message
    hashDecryptMsg = hash(str.encode(message))
    # compare the hash of decrypted message with received hash and output result
    print('\nHash Equal: {}'.format(hashDecryptMsg == hashMsg))

if __name__ == "__main__":
    verify('key.pem', 'ciphertext.txt')
        