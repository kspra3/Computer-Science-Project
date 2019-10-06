from bitstring import BitArray

def sellerInputStringToBin():
    sellerInputVal = str(input("Enter: "))
    sellerInputVal = BitArray(sellerInputVal.encode()).bin

    sWatermarkFile = open('sellerWatermark.txt', "w+")
    sWatermarkFile.write(sellerInputVal)
    sWatermarkFile.close()

if __name__== "__main__":
    sellerInputStringToBin()