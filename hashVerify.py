from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_512
from bitstring import BitArray
from base64 import b64encode, b64decode
import math

def hash(message):
    h_obj = SHA3_512.new()
    h_obj.update(message)
    return h_obj.hexdigest()

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def verify():
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

    with open('hashMsg.txt','r') as hashfile:
        hashMsg = hashfile.read()
    hashDecryptMsg = hash(str.encode(message))
    print('Hash Equal: {}'.format(hashDecryptMsg == hashMsg))

if __name__ == "__main__":
    verify()
        