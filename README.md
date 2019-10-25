# README.md

# End User Guide

## Guidelines/ Steps to run the program
1. Run main.py

2. Program prompts the user to choose between 1 (whole simulation of buyer-seller scenario) or 2 (verfication of the culprit).
   
### If the user chooses 1 (whole simulation of buyer-seller scenario)
3. Program prompts the user for buyer's watermark.

4. Program prompts the user for seller's watermark.

5. Program asks the user to enter the name of the original image.

6. Program asks the user to enter the name for the watermarked image.

7. Program generates watermarked image that has the name given by the user along with the buyer and seller watermarks embedded into it.

### If the user chooses 2 (verification of the culprit)
3. Program promts the user (Seller) for the name of watermarked image.

4. Program asks the user (Buyer) for the name of the file that contains the buyer's encrypted watermark.

5. Program asks the user (Seller) for the name of the file that contains the seller's encrypted watermark.

6. Program requests the user (Buyer) for the name of the file that contains the buyer's watermark.

7. Program requests the user (Seller) for the name of the file that contains the seller's watermark.

8. Program verifies for the presence of seller's and buyer's watermark within the watermarked image given by the user.

# Technical User Guide

## Software requirements
1. Matlab release R2019a

2. The python interpreter version 3.7 64-bit is needed to run the program and install required libraries (The 64-bit python interpreter is required for everything to work, a 32-bit version will not work). 

## Libraries/ Modules
The following libraries are not part of the standard python library and needed to be download separately.

### pycryptodome
This library can be installed in the command prompt using the following command.

```
pip install pycryptodome
```

### bitstring
This library can be installed in the command prompt using the following command.

```
pip install bitstring
```

### matlab.engine
To install this package, Matlab R2019a needs to be installed. Administrator privileges might be needed to execute the following commands. 

To install using the Windows command prompt, run the following commands.

```
cd "matlabroot\extern\engines\python"
python setup.py install
```

To install using the macOs or Linux command prompt, run the following commands.

```
cd "matlabroot/extern/engines/python"
python setup.py install
```

To install using the MATLAB command prompt, run the following commands.
```
cd (fullfile(matlabroot,'extern','engines','python'))
system('python setup.py install')
```

For more information on installing the matlab.engine package, visit [here](https://au.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html).

# Limitations of the code
- Discrete Cosine Transform (DCT) watermark embedding technique used in our program is not robust against image resizing. Hence, it restricts us from using Social Networking Services that resizes the image. This limits the size of the image to be watermarked to be not greater than 1200px * 1200px as Tumblr only accept image up to size 1280px * 1280px else it would resize the image and this will cause the watermark embedded into the image to be removed as discrete cosine transform is not tolerant against image resizing.

- Size of the watermark to be inserted heavily depends on the size of the image given. Our program will not be able to embeds the buyer's and the seller's watermark if the summation of the size of both watermarks is greater than the size of the image. However, this can be easily fixed by using a image with larger size.

- Reliance in the involvement of trusted third party in order to verify watermarks embedded in the watermarked image belongs to the seller and the buyer. Information stored within watermarks are available to trusted third party, therefore privacy of buyer's information is not protected.

- Currently, our program can only embed information in images with equal width and height.

# Potential Improvements and Further Work
- Apply Discrete Fourier Transform (DFT) to solve the resizing vulnerability in order to allow our program to be used across all Social Networking Services.

- Implement Homomorphic Encryption to allows the use of the Encrypt Then Insert method. This preserves the privacy and confidentiality of the buyer's and the seller's watermark as both buyer and seller could perform operations such as inserting their watermark after they have encrypted the components within the image.

# Considerations:
## Robustness:
- User's inputs are properly checked and handled using IF-ElSE conditions.
- Exception handling is done in order to detect incorrect filename that is provided by the user using TRY-EXCEPT blocks.
## Scalability:
- Our program is able to run watermark embedding and extracting for image of any size.
## Platform and OS independence:
- Our program works for any Windows, Linux and MacOS as long as it has access to the softwares and modules that we have specified under the software requirement and the libraries/ modules sections.
## Security:
- Asymmetric Rivest-Shamir-Adleman (RSA) encryption is used in our program to preserves the non-framing and non-repudation security properties that the buyer-seller watermarking protocol possessed and the confidentiality of buyer's and seller's watermarks that were embedded within the watermarked image. SHA-3 (Secure Hash Algorithm 3) is used by the seller for the authentication of the information received from the Buyer.
