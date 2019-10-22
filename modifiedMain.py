import matlab.engine
import os
import encryptRSA
import decryptRSA
import generateKeys
import hashVerify

cwd = os.path.dirname(os.path.abspath(__file__))
eng = matlab.engine.start_matlab()
eng.cd(cwd, nargout=0)

buyerKey = 'buyer.pem'
sellerKey = 'seller.pem'
buyerCipherFile = 'buyerCipher.txt'
sellerCipherFile = 'sellerCipher.txt'

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
print("################################################################################################################################")

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
hashVerifyReturnValue = hashVerify.verify(buyerKey, buyerCipherFile)

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

    bWatermarkFile = buyerCipherFile
    sWatermarkFile = sellerCipherFile

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
    eng.EmbedDCT(bWatermarkFile, sWatermarkFile, oriImgFile, wImgName, nargout=0)
    print("Watermark is embedded\n")

    print("Seller sends the watermarked image over to trusted third party along with the seller's watermark")
    print("Buyer will also sends the the watermark over to trusted third party")
    print("To verify that the watermarks that were embedded in the watermarked image belong to the buyer and the seller")
    print("################################################################################################################################")

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
    extractDCTReturnValue = eng.ExtractDCT(bWatermarkFile, sWatermarkFile, wImgName, nargout=0)
    print("Watermarks are extracted\n")

    if extractDCTReturnValue == 0:
        print("Extracted watermarks DOES NOT MATCH with the watermarks embedded")
        print("Program will now exit")
    else:
        print("Extracted watermarks MATCH with the watermarks embedded\n")

        buyerExtractedFile = "extracted_" + buyerCipherFile
        sellerExtractedFile = "extracted_" + sellerCipherFile

        print("Trusted third party decrypts the extracted watermark using Seller's and Buyer's Public Key")
        """
        RSA Decryption is done to the Encrypted Buyer's and Seller's Watermark using their respective Public Key
        Returns:
        1. 0 or 1 value indicating whether the decrypted value matches with the watermarks given by buyer and seller
           0 = Does not match
           1 = Matched
        """
        print("Start Decrypting the Extracted Encrypted Watermarks of Buyer and Seller")
        decryptRSAReturnValueBuyer = decryptRSA.decryptRSA(buyerKey, buyerCipherFile)
        decryptRSAReturnValueSeller = decryptRSA.decryptRSA(sellerKey, sellerCipherFile)
        print("Decryption is done\n")

        if (decryptRSAReturnValueBuyer == 1 and decryptRSAReturnValueSeller == 1):
            print("The Decrypted values MATCH with the watermarks given by buyer and seller\n")

            print("Trusted third party will then send the watermarked image to the buyer")
            print("Reached the end of the program, It will now exit")
        else:
            print("The decrypted values DOES NOT MATCH with the watermarks given by buyer and seller")
            print("Program will now exit")

"""
print("Seller extracts both watermarks out in order to ensure that the watermarks are correctly embedded into the image")
    print("Watermark extracting starts")
    # Extract both watermarks
    # Returns:
    # 1. 0 or 1 value indicating whether the extracted watermarks matches with the watermarks embedded by the seller
    #    0 = Does not match
    #    1 = Matched
    extractDCTReturnValue = eng.ExtractDCT(bWatermarkFile, sWatermarkFile, wImgName, nargout=0)
    print("Watermark is extracted\n")
    
    if extractDCTReturnValue == 0:
        print("Extracted watermarks DOES NOT MATCH with the watermarks embedded by the seller")
        print("Program will now exit")
    else:
        print("Extracted watermarks MATCH with the watermarks embedded by the seller\n")

        buyerExtractedFile = "extracted_" + buyerCipherFile
        sellerExtractedFile = "extracted_" + sellerCipherFile
        
        print("Seller decrypts the extracted watermark using Seller's and Buyer's Public Key")
        # RSA Decryption is done to the Encrypted Buyer's and Seller's Watermark using their respective Public Key
        # Returns:
        # 1. 0 or 1 value indicating whether the decrypted value matches with the watermarks given by buyer and seller
        #    0 = Does not match
        #    1 = Matched
        print("Start Decrypting the Extracted Encrypted Watermarks of Buyer and Seller")
        decryptRSAReturnValueBuyer = decryptRSA.decryptRSA(buyerKey, buyerCipherFile)
        decryptRSAReturnValueSeller = decryptRSA.decryptRSA(sellerKey, sellerCipherFile)
        print("Decryption is done\n")

        if (decryptRSAReturnValueBuyer == 1 and decryptRSAReturnValueSeller == 1):
            print("The Decrypted values MATCH with the watermarks given by buyer and seller\n")

            print("Seller sends the watermarked image over to Trusted Third Party along with the seller's watermark")
            print("Buyer will also sends the the watermark over to Trusted Third Party")
            print("To Verify that the watermarks that were embedded in the watermarked image belong to the buyer and the seller")
            print("################################################################################################################################")

            print("Trusted third party receives the watermarked image and seller's watermark from the seller")
            print("Trusted third party also receives buyer's watermark from the buyer")
            print("Trusted third party checks whether the watermarks in the image belong to the buyer and the seller")
            # Extract both watermarks
            # Returns:
            # 1. 0 or 1 value indicating whether the extracted watermarks matches with the watermarks embedded by the seller
            #    0 = Does not match
            #    1 = Matched
            extractDCTReturnValue = eng.ExtractDCT(bWatermarkFile, sWatermarkFile, wImgName, nargout=0)
        else:
            print("The Decrypted values DOES NOT MATCH with the watermarks given by buyer and seller")
            print("Program will now Exit")
"""
