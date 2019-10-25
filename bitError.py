def bitError(str1, str2):
    """
    Compute the bit error rate between two strings.

    parameters:
    str1 (string): First string to be compared
    str2 (string): Second string to be compared

    return value:
    (int) the bit error rate of two strings in percent
    """
    lenStr1 = len(str1)
    lenStr2 = len(str2)

    if lenStr1 != lenStr2:
        print("Inputs are of unequal length.")
        return
    else:
        count = 0
        for i in range(lenStr1):
            if str1[i] != str2[i]:
                count += 1
        return str((count/lenStr1) * 100) + "%"