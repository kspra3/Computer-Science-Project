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
oriImgFile = "Lenna.jpg"
wImgName = "Lenna2.jpg"

generateKeys.generateKeys(buyerKey)
generateKeys.generateKeys(sellerKey)

encryptRSA.encryptRSA(buyerKey, buyerCipherFile)
encryptRSA.encryptRSA(sellerKey, sellerCipherFile)

# verify buyer's identity
hashVerify.verify(buyerKey, buyerCipherFile)

bWatermarkFile = buyerCipherFile
sWatermarkFile = sellerCipherFile
eng.EmbedDCT(bWatermarkFile, sWatermarkFile, oriImgFile, wImgName, nargout=0)
eng.ExtractDCT(bWatermarkFile, sWatermarkFile, wImgName, nargout=0)

buyerExtractedFile = "extracted_" + buyerCipherFile
sellerExtractedFile = "extracted_" + sellerCipherFile
decryptRSA.decryptRSA(buyerKey, buyerCipherFile)
decryptRSA.decryptRSA(sellerKey, sellerCipherFile)

