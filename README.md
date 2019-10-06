FIT3162 Computer Science Project 2019 Semester 2
====================================================

Group 9
-----------

**Buyer Seller Watermarking Protocol**

1. Obtain the *Buyer*'s personal details. Write it into a text file using the Python file. An RSA encryption is then performed on the Buyer’s details where we accept the Buyer’s personal information as input and encrypt the information using the Buyer’s private key. The output is then saved into a text file.


2. The *Seller*'s watermark and the image is then obtained. The *Seller*’s watermark is then written into a text file in Python. The name of the image is also written into a text file. We then obtain the encrypted version of the *Buyer*’s personal information from the step above and decrypt it to verify the *Buyer*’s identity.


3. MATLAB(Data Hiding and extracting).

   The files we will be working with are the *Buyer*’s personal information (encrypted), the *Seller*’s watermark (both of these are in separate text files) and the JPEG image we would be watermarking.  
   
   Run the program for data embedding where both the encrypted *Buyer*’s personal information and the *Seller*’s watermark are hidden within the image using the __Discrete Cosine Transform(DCT).__
   
   The output is the watermarked image that we would like to Sell.  
   
   The watermarked image is then uploaded to __Tumblr__ (social media) and downloaded from there to test the image and the watermark's quality after going through Tumblr’s image processing protocols.  
   
   We extract the information hidden in the image. This will be the encrypted *Buyer*’s personal details and the *Seller*’s watermark which will both be separately saved into text files.  
   
   The *Buyer*’s personal details are obtained by decrypting the encrypted file and saved into a new text file.

4. Comparison (Bit Error Rate, SME, SSIM, PSNR)

   The integrity and viability of the entire process is tested here by comparing the files before going through data hiding and social media image processing and after they have.  
   
   The original and extracted Buyer’s personal details, the original and extracted encrypted Buyer’s personal detail and the original and extracted Seller’s watermark are all compared to using the Bit Error Rate and the Mean Squared Error.  
   
   The original image and the watermarked image are compared using SSIM and PSNR.


**Software and Platform**

1. Python 64-bits

2. Python Intepreter 64-bits (https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe)

3. MATLAB


**Modules**

1. Python: *Pycryptodome*, *Bitstring*, *Matlab.engine* and *OS*

2. MATLAB: *DCT* and *DWT*


**Input and Output**

Input: Image, String (Buyer’s Personal Details), String (Seller’s Watermark).

Output: Watermarked Image, String (Buyer’s Encrypted Information), String (extracted Buyer’s Personal Details), String (extracted Buyer’s Encrypted Information), String (extracted Seller’s Watermark).


**Limitations**

1. The DCT data hiding method is not robust against image resizing.

2. The block container that is used to store the watermark in DCT has to be multiple of 4, except for 8 since JPEG image compression uses a block size of 8x8.

3. The image needs to be bigger than a required size. This is because DWT requires a bigger image size to function properly and secondly the encrypted information is quite lengthy.


**Additional Information**

Two different methods, *DCT* and *DWT* were used to embed the watermarks. One method for each watermark.  
   
   Result: The quality of the watermark extracted from the watermarked image is poor.  
   
   Reasoning: The information of the first watermark is overridden by the second watermark.  
   
   Conclusion: Using the data embedding techniques that work in the same domain and frequency will lead to a huge loss in the information of the watermarks that are embedded.  
   
   Solution: Using the same data embedding techniques (*DCT* and *DWT*), but embed the watermarks into different frequency. Using one data embedding technique (*DCT* or *DWT*) and split the image into half in order to store both watermarks (one in the upper half and the other one in the lower half).

