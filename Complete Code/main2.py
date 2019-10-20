import matlab.engine
import os
import encryptRSA
import decryptRSA2
import generateKeys
import hashVerify

cwd = os.path.dirname(os.path.abspath(__file__))
eng = matlab.engine.start_matlab()
eng.cd(cwd, nargout=0)

fname=str(input("Enter the file name: "))

buyerKey = 'buyer.pem'
sellerKey = 'seller.pem'
buyerCipherFile = 'buyerCipher.txt'
sellerCipherFile = 'sellerCipher.txt'

bWatermarkFile = buyerCipherFile
sWatermarkFile = sellerCipherFile

eng.ExtractDCT(bWatermarkFile, sWatermarkFile, fname, nargout=0)
with open('extracted_buyerCipher.txt', 'r') as extracted_buyer_watermark:
    extractedBuyerValue = extracted_buyer_watermark.read()

with open('extracted_sellerCipher.txt', 'r') as extracted_seller_watermark:
    extractedSellerValue = extracted_seller_watermark.read()

with open('buyerCipher.txt', 'r') as buyer_cipher:
    buyerValue = buyer_cipher.read()

with open('sellerCipher.txt', 'r') as seller_cipher:
    sellerValue = seller_cipher.read()

if (buyerValue == extractedBuyerValue) and (sellerValue == extractedSellerValue):
    buyerExtractedFile = "extracted_" + buyerCipherFile
    sellerExtractedFile = "extracted_" + sellerCipherFile
    decryptRSA2.decryptRSA2(buyerKey, buyerCipherFile)
    decryptRSA2.decryptRSA2(sellerKey, sellerCipherFile)
else:
    print("The information extracted does not match with the original cipher text")
    print("Buyer Watermark: " + str(buyerValue))
    print("Extracted Buyer Watermark: " + str(extractedBuyerValue))
    print("Seller Watermark: " + str(sellerValue))
    print("Extracted Seller Watermark: " + str(extractedSellerValue))

