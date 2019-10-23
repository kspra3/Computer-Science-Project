import unittest
from unittest.mock import Mock, patch
from decryptRSA import decryptRSA, decrypt
from encryptRSA import encryptRSA, encrypt
from hashVerify import hash, verify, bitstring_to_bytes
from generateKeys import generateKeys, newkeys
from Crypto.PublicKey import RSA
import os


class pyTest(unittest.TestCase):
    @classmethod
    def tearDownClass(self):
        files = ['hash_out.txt','hash_out2.txt','origin_out.txt','origin_out2.txt','origin.txt','out.txt','out2.txt','temp.PEM','temp2.PEM']
        for f in files:
            os.remove(f)


    # testing different keys are generated each time
    def test_newkeys_len(self):
        keysize = 1024
        key1 = newkeys(keysize)
        key2 = newkeys(keysize)
        self.assertNotEqual(key1, key2)
    
    # testing keys are written correctly into file
    def test_genkeys_write(self):
        kfilename = "temp.PEM"
        generateKeys(kfilename)
        with open(kfilename, mode='r') as keyfile:
            try:
                key = RSA.import_key(keyfile.read())
            except:
                self.fail("generateKeys raises unexpected exception.")
    
    # testing string is encrypted 
    def test_encrypt(self):
        msg = str.encode("Hello there")
        kfilename = "temp.PEM"

        with open(kfilename, mode='r') as keyfile:
            key = RSA.import_key(keyfile.read()) 

        ciphertext = encrypt(msg, key)
        self.assertNotEqual(ciphertext, msg)

    # testing same keys yield different ciphertext, due to random padding
    def test_encrypt_multiple_samekey(self):
        msg = str.encode("Hello there")
        kfilename = "temp.PEM"

        with open(kfilename, mode='r') as keyfile:
            key = RSA.import_key(keyfile.read()) 

        ciphertext = encrypt(msg, key)
        ciphertext2 = encrypt(msg, key)
        self.assertNotEqual(ciphertext,ciphertext2)

    # testing different keys yield different ciphertext
    def test_encrypt_multiple_diffkey(self):
        msg = str.encode("Hello there")
        kfilename = "temp.PEM"
        kfilename2 = "temp2.PEM"

        generateKeys(kfilename2)

        with open(kfilename, mode='r') as keyfile:
            key = RSA.import_key(keyfile.read()) 
        with open(kfilename2, mode='r') as keyfile:
            key2 = RSA.import_key(keyfile.read()) 
        ciphertext = encrypt(msg, key)
        ciphertext2 = encrypt(msg, key2)
        self.assertNotEqual(ciphertext,ciphertext2)
    
    # when correct ciphertext and key is used, decrypted plaintext == original plaintext
    def test_decrypt_ccip_ckey(self):
        ori_msg = "Hello there"
        msg = str.encode(ori_msg)

        kfilename = "temp.PEM"

        with open(kfilename, mode='r') as keyfile:
            key = RSA.import_key(keyfile.read()) 
        ciphertext = encrypt(msg, key)
        plaintext = decrypt(ciphertext, key).decode("ascii")
        self.assertEqual(ori_msg, plaintext)

    # when correct ciphertext and wrong key is used, decryption will fail
    def test_decrypt_ccip_wkey(self):
        ori_msg = "Hello there"
        msg = str.encode(ori_msg)

        kfilename = "temp.PEM"
        generateKeys(kfilename)

        kfilename2 = "temp2.PEM"
        generateKeys(kfilename2)

        with open(kfilename, mode='r') as keyfile:
            key = RSA.import_key(keyfile.read()) 
        with open(kfilename2, mode='r') as keyfile:
            key2 = RSA.import_key(keyfile.read()) 
        ciphertext = encrypt(msg, key)
        with self.assertRaises(ValueError):
            plaintext = decrypt(ciphertext, key2)
    
    # hashes of two same strings should be equal
    def test_hash_equal(self):
        msg = str.encode("Hello there")
        hash_msg = hash(msg)
        hash_msg2 = hash(msg)
        self.assertEqual(hash_msg, hash_msg2)
    
    # hashes of two different strings should not match
    def test_hash_notequal(self):
        msg = str.encode("Hello there")
        msg2 = str.encode("Hello world")
        hash_msg = hash(msg)
        hash_msg2 = hash(msg2)
        self.assertNotEqual(hash_msg, hash_msg2)

    # test that bitstring_to_bytes output is of type bytes
    def test_bitstring2bytes(self):
        string = "10000000"
        output = bitstring_to_bytes(string)
        self.assertEqual(type(output), bytes)        

    # test that ciphertext is correctly written into file 
    @patch('builtins.input')
    def test_encryptRSA(self, inp):
        msg = "hello there"
        keyfile = "temp.PEM"
        outfile = "out.txt"

        inp.return_value = msg
        encryptRSA(keyfile, outfile)
        with open(outfile, mode='r') as cipherfile:
            try:
                ciphertext = cipherfile.read()
                self.assertGreater(len(ciphertext),0)
            except:
                self.fail("encryptRSA raises unexpected exception.")

    # test that when the correct ciphertext and key is read in, decrypted plaintext matches original plaintext
    @patch('builtins.input')
    def test_decryptRSA_cc_ck(self, inp):
        msg = "hello there"
        keyfile = "temp.PEM"
        ciphertextfile = "out.txt"
        originFilename = "origin.txt"
        generateKeys(keyfile)

        inp.return_value = msg
        encryptRSA(keyfile, ciphertextfile)
        
        with open(originFilename, mode="w") as ofile:
            ofile.write(msg)
        retVal = decryptRSA(keyfile, ciphertextfile, originFilename)
        self.assertEqual(1, retVal[0])

    # test that when the wrong ciphertext and key is read in, decrypted plaintext does not matches original plaintext
    @patch('builtins.input')
    def test_decryptRSA_wc_ck(self, inp):
        msg = "hello there"
        msg2 = "good bye"

        keyfile = "temp.PEM"
        generateKeys(keyfile)
        ciphertextfile = "out.txt"
        ciphertextfile2 = "out2.txt"
        originFilename = "origin.txt"

        inp.return_value = msg
        encryptRSA(keyfile, ciphertextfile)
        inp.return_value = msg2
        encryptRSA(keyfile, ciphertextfile2)

        with open(originFilename, mode="w") as ofile:
            ofile.write(msg)
        retVal = decryptRSA(keyfile, ciphertextfile2, originFilename)
        self.assertEqual(0, retVal[0])

    # test that when decrypted plaintext hash is compared with the correct hash, the hashes match
    @patch('builtins.input')
    def test_verify_ch(self, inp):
        msg = "hello there"
        keyfile = "temp.PEM"
        outfile = "out.txt"
        hashfile = "hash_out.txt"
        generateKeys(keyfile)

        inp.return_value = msg
        encryptRSA(keyfile,outfile)
        retVal = verify(keyfile,outfile,hashfile)
        self.assertEqual(1, retVal)

    # test that when decrypted plaintext hash is compared with the wrong hash, the hashes don't match
    @patch('builtins.input')
    def test_verify_wh(self, inp):
        msg = "hello there"
        msg2 = "good bye"
        keyfile = "temp.PEM"
        outfile = "out.txt"
        outfile2 = "out2.txt"
        hashfile2 = "hash_out2.txt"
        generateKeys(keyfile)

        inp.return_value = msg
        encryptRSA(keyfile,outfile)

        inp.return_value = msg2
        encryptRSA(keyfile,outfile2)

        retVal = verify(keyfile,outfile,hashfile2)
        self.assertEqual(0, retVal)


if __name__ == "__main__":
    unittest.main()