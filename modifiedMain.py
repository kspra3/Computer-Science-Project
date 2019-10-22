import matlab.engine
import os
import encryptRSA
import decryptRSA
import generateKeys
import hashVerify
import sys

cwd = os.path.dirname(os.path.abspath(__file__))
eng = matlab.engine.start_matlab()
eng.cd(cwd, nargout=0)

buyerKey = 'buyer.pem'
sellerKey = 'seller.pem'
buyerCipherFile = 'buyerCipher.txt'
sellerCipherFile = 'sellerCipher.txt'

bWatermarkFile = buyerCipherFile
sWatermarkFile = sellerCipherFile

buyerExtractedFile = "extracted_" + buyerCipherFile
sellerExtractedFile = "extracted_" + sellerCipherFile
buyerOriginfilename = "origin_" + buyerCipherFile
sellerOriginfilename = "origin_" + sellerCipherFile

print("Choose Y for the whole simulation of buyer-seller scenario")
print("Choose N for verification of the culprit")
userInput = str(input("Enter (Y/N): "))

if (userInput == 'Y'):
    # Buyer Side
    """
    Generates Public and Private Key Pairs
    Returns:
    1. Generated Key Pairs - saved into 'buyer.pem' file
    """
    print("Buyer generates the public and private key pairs")
    generateKeys.generateKeys(buyerKey)
    print("Buyer's public and private key pairs is generated\n")

    """
    Prompts Buyer for watermark
    RSA Encryption is done using Buyer's Private Key
    Returns:
    1. Encrypted Watermark - saved into 'buyerCipher.txt' file
    2. Buyer's Hash - saved into 'hash_buyerCipher.txt' file
    """
    print("Buyer will now insert the watermark")
    encryptRSA.encryptRSA(buyerKey, buyerCipherFile)
    print("Buyer's watermark is successfully encrypted with buyer's private key")
    print("Buyer's information hash is generated as well")
    print("Buyer sends the encrypted watermark and information hash over to the seller")
    print("")

    # Seller Side
    print("Seller receives buyer's encrypted watermark and information hash")

    """
    Verifies the authenticity of a ciphertext by decrypting the ciphertext,
    Computing its hash and comparing the computed hash against the received hash
    Returns:
    1. 0 or 1 value indicating whether the Buyer's hash information matches with
       the hash information produced by the Encrypted Watermark.
       0 = Does not match
       1 = Matched
    """
    print("Seller verifies buyer's identity")
    hashFilename = "hash_" + buyerCipherFile
    hashVerifyReturnValue = hashVerify.verify(buyerKey, buyerCipherFile, hashFilename)
    if hashVerifyReturnValue == 0:
        print("Buyer's hash information DOES NOT MATCH with the hash information produced by the encrypted watermark\n")
        print("Program will now exit")
    else:
        print("Buyer's hash information MATCHES with the hash information produced by the encrypted watermark\n")

        """
        Generates Public and Private Key Pairs
        Returns:
        1. Generated Key Pairs - saved into 'seller.pem' file
        """
        print("Seller generates the public and private key pairs")
        generateKeys.generateKeys(sellerKey)
        print("Seller's public and private key pairs is generated\n")

        """
        Prompts Seller for watermark
        RSA Encryption is done using Seller's Private Key
        Returns:
        1. Encrypted Watermark - saved into 'sellerCipher.txt' file
        2. Seller's Hash - saved into 'hash_sellerCipher.txt' file
        """
        print("Seller will now insert the watermark")
        encryptRSA.encryptRSA(sellerKey, sellerCipherFile)
        print("Seller's watermark is successfully encrypted with seller's private key")
        print("Seller's information hash is generated as well\n")

        print("Seller embeds both encrypted watermarks into an image that the buyer wants to purchase")
        print("Seller specify the name of the original image that the buyer wants to purchase")
        oriImgFile = str(input("Enter the name of the original image: "))
        print("Seller specify the name for the watermarked image that will be pass to the buyer")
        wImgName = str(input("Enter the name for the watermarked image: "))
        """
        Embed both watermarks into an image
        Returns:
        1. Watermarked Image
        """
        print("Watermark embedding starts")
        try:
            eng.EmbedDCT(bWatermarkFile, sWatermarkFile, oriImgFile, wImgName, nargout=0)
        except:
            print("File does not exist")
            print("Program will now exit")
            sys.exit()
            
        print("Watermark is embedded\n")

        print("Seller sends the watermarked image over to trusted third party along with the seller's watermark")
        print("Buyer will also sends the the watermark over to trusted third party")
        print("To verify that the watermarks that were embedded in the watermarked image belong to the buyer and the seller")
        print("")

        # Trusted Third Party Side
        print("Trusted third party receives the watermarked image and seller's watermark from the seller")
        print("Trusted third party also receives buyer's watermark from the buyer")
        print("Trusted third party checks whether the watermarks in the image belong to the buyer and the seller\n")

        print("Trusted third party extracts both watermarks out of the watermarked image")
        """
        Extract both watermarks
        Returns:
        1. 0 or 1 value indicating whether the extracted watermarks matches with the watermarks embedded by the seller
           0 = Does not match
           1 = Matched
        """
        print("Start extracting the watermarks")
        eng.ExtractDCT(bWatermarkFile, sWatermarkFile, wImgName, nargout=0)
        print("Watermarks are extracted\n")
        
        with open(buyerExtractedFile, 'r') as extracted_buyer_watermark:
            extractedBuyerWatermark = extracted_buyer_watermark.read()

        with open(sellerExtractedFile, 'r') as extracted_seller_watermark:
            extractedSellerWatermark = extracted_seller_watermark.read()

        with open(buyerCipherFile, 'r') as buyer_cipher:
            buyerEncryptedWatermark = buyer_cipher.read()

        with open(sellerCipherFile, 'r') as seller_cipher:
            sellerEncryptedWatermark = seller_cipher.read()
            
        if (buyerEncryptedWatermark != extractedBuyerWatermark or sellerEncryptedWatermark != extractedSellerWatermark):
            print("Extracted watermarks DOES NOT MATCH with the watermarks embedded")
            print("Program will now exit")
        else:
            print("Extracted watermarks MATCH with the watermarks embedded\n")

            print("Trusted third party decrypts the extracted watermark using Seller's and Buyer's Public Key")
            """
            RSA Decryption is done to the Encrypted Buyer's and Seller's Watermark using their respective Public Key
            Returns:
            1. 0 or 1 value indicating whether the decrypted value matches with the watermarks given by buyer and seller
               0 = Does not match
               1 = Matched
            """
            print("Start Decrypting the Extracted Encrypted Watermarks of Buyer and Seller")
            decryptRSAReturnValueBuyer = decryptRSA.decryptRSA(buyerKey, buyerCipherFile, buyerOriginfilename)
            decryptRSAReturnValueSeller = decryptRSA.decryptRSA(sellerKey, sellerCipherFile, sellerOriginfilename)
            print("Decryption is done\n")

            if (decryptRSAReturnValueBuyer == 1 and decryptRSAReturnValueSeller == 1):
                print("The decrypted values MATCH with the watermarks given by buyer and seller\n")

                print("Trusted third party will then send the watermarked image to the buyer")
                print("It has reached the end of the program and it will now exit")
            else:
                print("The decrypted values DOES NOT MATCH with the watermarks given by buyer and seller\n")

                print("Program will now exit")

elif (userInput == 'N'):
    watermarkedImageName = str(input("Enter the name of the watermarked image: "))
    buyerEncryptedWatermarkFN = str(input("Enter the filename that contains Buyer's Encrypted Watermark (buyerCipher.txt): "))
    sellerEncryptedWatermarkFN = str(input("Enter the filename that contains Seller's Encrypted Watermark (sellerCipher.txt): "))
    buyerWatermarkFN = str(input("Enter the filename that contains Buyer's Watermark (origin_buyerCipher.txt): "))
    sellerWatermarkFN = str(input("Enter the filename that contains Seller's Watermark (origin_sellerCipher.txt): "))

    print("Start extracting the watermarks")
    try:
        eng.ExtractDCT(bWatermarkFile, sWatermarkFile, watermarkedImageName, nargout=0)
    except:
        print("File does not exist")
        print("Program will now exit")
        sys.exit()
    print("Watermarks are extracted\n")
    
    with open(buyerExtractedFile, 'r') as extracted_buyer_watermark:
        extractedBuyerWatermark = extracted_buyer_watermark.read()

    with open(sellerExtractedFile, 'r') as extracted_seller_watermark:
        extractedSellerWatermark = extracted_seller_watermark.read()

    try:
        with open(buyerEncryptedWatermarkFN, 'r') as buyer_cipher:
            buyerEncryptedWatermark = buyer_cipher.read()
            #print(buyerEncryptedWatermark)
    except:
            print("File does not exist")
            print("Program will now exit")
            sys.exit()

    try:
        with open(sellerEncryptedWatermarkFN, 'r') as seller_cipher:
            sellerEncryptedWatermark = seller_cipher.read()
            #print(sellerEncryptedWatermark)
    except:
            print("File does not exist")
            print("Program will now exit")
            sys.exit()
    
    if (buyerEncryptedWatermark != extractedBuyerWatermark or sellerEncryptedWatermark != extractedSellerWatermark):
        print("The extracted ciphertext does not match the original ciphertext")
        print("Buyer Watermark: " + str(buyerEncryptedWatermark))
        print("Extracted Buyer Watermark: " + str(extractedBuyerWatermark))
        print("Seller Watermark: " + str(sellerEncryptedWatermark))
        print("Extracted Seller Watermark: " + str(extractedSellerWatermark))
        print("Program will now exit")
    else:
        try:
            decryptRSAReturnValueBuyer = decryptRSA.decryptRSA(buyerKey, buyerCipherFile, buyerWatermarkFN)
        except:
            print("File does not exist")
            print("Program will now exit")
            sys.exit()
            
        try:
            decryptRSAReturnValueSeller = decryptRSA.decryptRSA(sellerKey, sellerCipherFile, sellerWatermarkFN)
        except:
            print("File does not exist")
            print("Program will now exit")
            sys.exit()
            
        if (decryptRSAReturnValueBuyer == 1):
            print("The decrypted values MATCH with the suspected buyer's watermark")
            print("The buyer who has this watermark is the culprit who redistributed the image without the permission of the content owner\n")

            print("The program has reached the end and it will now exit")
        elif (decryptRSAReturnValueSeller == 1):
            print("The decrypted values MATCH with the seller's watermark")
            print("Proves that the seller is the owner of this image\n")

            print("The program has reached the end and it will now exit")
        elif (decryptRSAReturnValueBuyer == 0):
            print("The decrypted values DOES NOT MATCH with the suspected buyer's watermark")
            print("The suspected buyer is not the one who redistributed the image without the permission of the content owner\n")

            print("The program has reached the end and it will now exit")
        elif (decryptRSAReturnValueSeller == 0):
            print("The decrypted values MATCH with the seller's watermark")
            print("The seller is not the owner of this image\n")
            
            print("The program has reached the end and it will now exit")

else:
    print("Incorrect input!")
