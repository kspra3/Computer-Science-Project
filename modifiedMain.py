"""
Description: Main file that complies and runs all the python RSA encryption code and matlab DCT watermark embedding code in a single main.py script
Functions:
- To perform the whole simulation of buyer-seller scenario (Including trusted third party)
- To track and verify the culprit who redistributed the purchased image without the permission of the content owner (Seller)
Return: None
"""

import matlab.engine
import os
import encryptRSA
import decryptRSA
import generateKeys
import hashVerify
import sys
import bitError

cwd = os.path.dirname(os.path.abspath(__file__))
eng = matlab.engine.start_matlab()
eng.cd(cwd, nargout=0)

# filename of the file that contains buyer's public and private key
buyerKey = 'buyer.pem'
# filename of the file that contains seller's public and private key
sellerKey = 'seller.pem'
# filename of the file that contains the encrypted buyer's watermark
buyerCipherFile = 'buyerCipher.txt'
# filename of the file that contains the encrypted seller's watermark
sellerCipherFile = 'sellerCipher.txt'

# filename of the file that contains the encrypted buyer's watermark
bWatermarkFile = buyerCipherFile
# filename of the file that contains the encrypted buyer's watermark
sWatermarkFile = sellerCipherFile

# filename of the file that contains the extracted encrypted buyer's watermark
buyerExtractedFile = "extracted_" + buyerCipherFile
# filename of the file that contains the extracted encrypted seller's watermark
sellerExtractedFile = "extracted_" + sellerCipherFile
# filename of the file that contains the buyer's origin watermark
buyerOriginfilename = "origin_" + buyerCipherFile
# filename of the file that contains the seller's origin watermark
sellerOriginfilename = "origin_" + sellerCipherFile

# filename of the file that contains the hash of the buyer
hashFilename = "hash_" + buyerCipherFile

# Guiding the user to choose what they want this script to perform
print("Choose 1 for the whole simulation of buyer-seller scenario")
print("Choose 2 for verification of the culprit")
# Storing user input
userInput = str(input("Enter (1 or 2): "))

# Checking the user input to determine which method to run
if (userInput == '1'):
    # Simulation of buyer-seller scenario with the involvement of trusted third party

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
    hashVerifyReturnValue = hashVerify.verify(buyerKey, buyerCipherFile, hashFilename)

    if hashVerifyReturnValue == 0:
        # Handling the case where the hash information does not belongs to the buyer
        print("Buyer's hash information DOES NOT MATCH with the hash information produced by the encrypted watermark\n")
        print("Program will now exit")
    else:
        # Handling the case where the hash information verifies the buyer's identity
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
        # Name of the original image
        oriImageName = str(input("Enter the name of the original image (Lenna.jpg): "))
        print("Seller specify the name for the watermarked image that will be pass to the buyer")
        # Name of the watermarked image with buyer's and seller's encrypted watermark
        wImageName = str(input("Enter the name for the watermarked image (must include .jpg): "))

        # Using exception handling to catch incorrect filename or file that does not exit
        try:
            """
            Embed both watermarks into an image
            Returns:
            1. Watermarked Image
            """
            eng.EmbedDCT(bWatermarkFile, sWatermarkFile, oriImageName, wImageName, nargout=0)
        except:
            print(str(oriImageName) + " image file does not exist. Try (Lenna.jpg)")
            print("Program will now exit")
            sys.exit()

        print("Watermark embedding starts")
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
        eng.ExtractDCT(bWatermarkFile, sWatermarkFile, wImageName, nargout=0)
        print("Watermarks are extracted\n")

        # Open the file that contains extracted encrypted buyer's watermark and read it into extractedBuyerWatermark
        with open(buyerExtractedFile, 'r') as extracted_buyer_watermark:
            extractedBuyerWatermark = extracted_buyer_watermark.read()

        # Open the file that contains extracted encrypted seller's watermark and read it into extractedSellerWatermark
        with open(sellerExtractedFile, 'r') as extracted_seller_watermark:
            extractedSellerWatermark = extracted_seller_watermark.read()

        # Open the file that contains encrypted buyer's watermark and read it into buyerEncryptedWatermark
        with open(buyerCipherFile, 'r') as buyer_cipher:
            buyerEncryptedWatermark = buyer_cipher.read()

        # Open the file that contains encrypted seller's watermark and read it into sellerEncryptedWatermark
        with open(sellerCipherFile, 'r') as seller_cipher:
            sellerEncryptedWatermark = seller_cipher.read()

        if (buyerEncryptedWatermark != extractedBuyerWatermark or sellerEncryptedWatermark != extractedSellerWatermark):
            # Handling the cases where the encrypted buyer's watermark does not match the extracted buyer's watermark
            # or the encrypted seller's watermark does not match the extracted seller's watermark
            print("Extracted watermarks DOES NOT MATCH with the watermarks embedded")
            print("Program will now exit")
        else:
            # Handling the case where both encrypted buyer's and seller's watermark match the extracted buyer's and seller's watermark
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
            decryptRSAReturnArrayBuyer = decryptRSA.decryptRSA(buyerKey, buyerCipherFile, buyerOriginfilename)
            decryptRSAReturnArraySeller = decryptRSA.decryptRSA(sellerKey, sellerCipherFile, sellerOriginfilename)
            print("Decryption is done\n")

            if (decryptRSAReturnArrayBuyer[0] == 1 and decryptRSAReturnArraySeller[0] == 1):
                # Handling the cases where the decrypted values match with the buyer's and seller's watermark
                print("The decrypted values MATCH with the watermarks given by buyer and seller")
                print("Buyer's Watermark: " + decryptRSAReturnArrayBuyer[1])
                print("Extracted Buyer's Watermark: " + decryptRSAReturnArrayBuyer[2])
                print("Seller's Watermark: " + decryptRSAReturnArraySeller[1])
                print("Extracted Seller's Watermark: " + decryptRSAReturnArraySeller[2])
                print("\nTrusted third party will then send the watermarked image to the buyer\n")
                print("It has reached the end of the program and it will now exit\n")

                print("Comparison between the quality of original image and watermarked image:")
                readingPSNR = eng.getPSNR(oriImageName, wImageName, nargout=1)
                readingSSIM = eng.getSSIM(oriImageName, wImageName, nargout=1)
                print("PSNR Value: " + str(readingPSNR))
                print("SSIM Value: " + str(readingSSIM * 100) + "%")
                print("")

                print("Comparison between the encrypted watermark and the extracted encrypted watermark using Bit Error Rate")
                readingBitErrorRate_Buyer = bitError.bitError(buyerEncryptedWatermark, extractedBuyerWatermark)
                readingBitErrorRate_Seller = bitError.bitError(sellerEncryptedWatermark, extractedSellerWatermark)
                print("Bit Error Rate Value (Buyer): " + str(readingBitErrorRate_Buyer))
                print("Bit Error Rate Value (Seller): " + str(readingBitErrorRate_Seller))
            else:
                # Handling the cases where the decrypted values does not match with the buyer's and seller's watermark
                print("The decrypted values DOES NOT MATCH with the watermarks given by buyer and seller")
                print("Buyer's Watermark: " + decryptRSAReturnArrayBuyer[1])
                print("Extracted Buyer's Watermark: " + decryptRSAReturnArrayBuyer[2])
                print("Seller's Watermark: " + decryptRSAReturnArraySeller[1])
                print("Extracted Seller's Watermark: " + decryptRSAReturnArraySeller[2])
                print("\nProgram will now exit")

                print("Comparison between the quality of original image and watermarked image:")
                readingPSNR = eng.getPSNR(oriImageName, wImageName, nargout=1)
                readingSSIM = eng.getSSIM(oriImageName, wImageName, nargout=1)
                print("PSNR Value: " + str(readingPSNR))
                print("SSIM Value: " + str(readingSSIM * 100) + "%")
                print("")

                print("Comparison between the encrypted watermark and the extracted encrypted watermark using Bit Error Rate")
                readingBitErrorRate_Buyer = bitError.bitError(buyerEncryptedWatermark, extractedBuyerWatermark)
                readingBitErrorRate_Seller = bitError.bitError(sellerEncryptedWatermark, extractedSellerWatermark)
                print("Bit Error Rate Value (Buyer): " + str(readingBitErrorRate_Buyer))
                print("Bit Error Rate Value (Seller): " + str(readingBitErrorRate_Seller))

elif (userInput == '2'):
    # Culprit verification

    # Prompt the user to input the name of the watermarked image with buyer's and seller's encrypted watermark
    watermarkedImageName = str(input("Enter the name of the watermarked image (Lenna2.jpg): "))

    print("Begin extraction of watermarks")
    # Using exception handling to catch incorrect filename or file that does not exit
    try:
        # This function extracts the both buyer's and seller's watermark from the watermarked image
        eng.ExtractDCT(bWatermarkFile, sWatermarkFile, watermarkedImageName, nargout=0)
    except:
        print("(" + str(watermarkedImageName) + ")" + " watermarked image does not exist. Try (Lenna2.jpg)")
        print("Program exiting.")
        sys.exit()

    print("Watermarks are extracted\n")

    # Open the file that contains extracted encrypted buyer's watermark and read it into extractedBuyerWatermark
    with open(buyerExtractedFile, 'r') as extracted_buyer_watermark:
        extractedBuyerWatermark = extracted_buyer_watermark.read()

    # Open the file that contains extracted encrypted seller's watermark and read it into extractedSellerWatermark
    with open(sellerExtractedFile, 'r') as extracted_seller_watermark:
        extractedSellerWatermark = extracted_seller_watermark.read()

    # filename of the file that contains the encrypted buyer's watermark
    buyerEncryptedWatermarkFN = str(input("Enter the filename that contains Buyer's Encrypted Watermark (buyerCipher.txt): "))
    # Using exception handling to catch incorrect filename or file that does not exit
    try:
        # Open the file that contains the encrypted buyer's watermark and read it into buyerEncryptedWatermark
        with open(buyerEncryptedWatermarkFN, 'r') as buyer_cipher:
            buyerEncryptedWatermark = buyer_cipher.read()
    except:
        print("(" + str(buyerEncryptedWatermarkFN) + ")" + " buyer's encrypted watermark file does not exist. Try (buyerCipher.txt)")
        print("Program will now exit")
        sys.exit()

    # filename of the file that contains the encrypted seller's watermark
    sellerEncryptedWatermarkFN = str(input("Enter the filename that contains Seller's Encrypted Watermark (sellerCipher.txt): "))
    # Using exception handling to catch incorrect filename or file that does not exit
    try:
        # Open the file that contains the encrypted seller's watermark and read it into sellerEncryptedWatermark
        with open(sellerEncryptedWatermarkFN, 'r') as seller_cipher:
            sellerEncryptedWatermark = seller_cipher.read()
    except:
        print("(" + str(sellerEncryptedWatermarkFN) + ")" + " seller's encrypted watermark file does not exist. Try (sellerCipher.txt)")
        print("Program will now exit")
        sys.exit()
    
    if (buyerEncryptedWatermark != extractedBuyerWatermark or sellerEncryptedWatermark != extractedSellerWatermark):
        # Handling the cases where the encrypted buyer's watermark does not match the extracted buyer's watermark
        # or the encrypted seller's watermark does not match the extracted seller's watermark
        print("\nThe extracted ciphertext does not match the original ciphertext")
        print("Buyer Watermark: " + str(buyerEncryptedWatermark))
        print("Extracted Buyer Watermark: " + str(extractedBuyerWatermark))
        print("Seller Watermark: " + str(sellerEncryptedWatermark))
        print("Extracted Seller Watermark: " + str(extractedSellerWatermark))
        print("\nProgram will now exit")
    else:
        # Handling the case where both encrypted buyer's and seller's watermark match the extracted buyer's and seller's watermark

        # filename of the file that contains the buyer's watermark
        buyerWatermarkFN = str(input("Enter the filename that contains Buyer's Watermark (origin_buyerCipher.txt): "))
        # Using exception handling to catch incorrect filename or file that does not exit
        try:
            # This function decrypt the extracted encrypted buyer's watermark to extracted buyer's watermark
            decryptRSAReturnArrayBuyer = decryptRSA.decryptRSA(buyerKey, buyerCipherFile, buyerWatermarkFN)
        except:
            print("(" + str(buyerWatermarkFN) + ")" + " buyer's watermark file does not exist. Try (origin_buyerCipher.txt)")
            print("Program will now exit")
            sys.exit()

        # filename of the file that contains the seller's watermark
        sellerWatermarkFN = str(input("Enter the filename that contains Seller's Watermark (origin_sellerCipher.txt): "))
        # Using exception handling to catch incorrect filename or file that does not exit
        try:
            # This function decrypt the extracted encrypted seller's watermark to extracted seller's watermark
            decryptRSAReturnArraySeller = decryptRSA.decryptRSA(sellerKey, sellerCipherFile, sellerWatermarkFN)
        except:
            print("(" + str(sellerWatermarkFN) + ")" + " seller's watermark file does not exist. Try (origin_sellerCipher.txt)")
            print("Program will now exit")
            sys.exit()

        print("Start Decrypting the Extracted Encrypted Watermarks of Buyer and Seller")
        print("Decryption is done\n")
            
        if (decryptRSAReturnArrayBuyer[0] == 1):
            # Handling the case where the decrypted values MATCH with the suspected buyer's watermark
            print("\nThe decrypted values MATCH with the suspected buyer's watermark")
            print("Suspected buyer's watermark: " + str(decryptRSAReturnArrayBuyer[1]))
            print("Extracted watermark: " + str(decryptRSAReturnArrayBuyer[2]))
            print("The buyer with this watermark is the culprit who redistributed the image without the permission of the content owner")
        else:
            # Handling the case where the decrypted values DOES NOT MATCH with the suspected buyer's watermark
            print("\nThe decrypted values DOES NOT MATCH with the suspected buyer's watermark")
            print("Suspected buyer's watermark: " + str(decryptRSAReturnArrayBuyer[1]))
            print("Extracted watermark: " + str(decryptRSAReturnArrayBuyer[2]))
            print("The suspected buyer is not the one who redistributed the image without the permission of the content owner")
        if (decryptRSAReturnArraySeller[0] == 1):
            # Handling the case where the decrypted values MATCH with the seller's watermark
            print("\nThe decrypted values MATCH with the seller's watermark")
            print("Seller's watermark: " + str(decryptRSAReturnArraySeller[1]))
            print("Extracted watermark: " + str(decryptRSAReturnArraySeller[2]))
            print("Proves that the seller is the owner of this image")
        else:
            # Handling the case where the decrypted values DOES NOT MATCH with the seller's watermark
            print("\nThe decrypted values DOES NOT MATCH with the seller's watermark")
            print("Seller's watermark: " + str(decryptRSAReturnArraySeller[1]))
            print("Extracted watermark: " + str(decryptRSAReturnArraySeller[2]))
            print("The seller is not the owner of this image")
            
        print("\nThe program has reached the end and it will now exit")

else:
    # Handling the case where user input anything other than 1 or 2
    print("Incorrect input!")
