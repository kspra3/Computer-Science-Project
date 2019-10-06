def binaryToString(input):
    sWatermarkFile = open(input, "r")
    for char in sWatermarkFile:
        value = bitstring_to_bytes(char).decode("ascii")
    print(value)

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

if __name__== "__main__":
    binaryToString('sellerWatermark.txt')