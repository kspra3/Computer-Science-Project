# README.md

# End User Guide

## Guideline/Step to run the program
1. Run main.py

2. Program prompts the user to choose between 1 (whole simulation of buyer-seller scenario) or 2 (verfication of the culprit).
   
### If the user chooses 1 (whole simulation of buyer-seller scenario)
3. Program prompts the user for buyer's watermark.

4. Program prompts the user for seller's watermark.

5. Program asks the user to enter the name of the original image.

6. Program asks the user to enter the name for the watermarked image.

7. Program generates watermarked image that has the given by the user with buyer and seller watermarks embedded into it.

### If the user chooses 2 (verification of the culprit)
3. Program promts the user (Seller) for the name of watermarked image.

4. Program asks the user (Buyer) for the name of the file that contains the buyer's encrypted watermark.

5. Program asks the user (Seller) for the name of the file that contains the seller's encrypted watermark.

6. Program requests the user (Buyer) for the name of the file that contains the buyer's watermark.

7. Program requests the user (Seller) for the name of the file that contains the seller's watermark.

8. Program verifies for the presence of seller's and buyer's watermark within the watermarked image given by the user.

# Technical User Guide

## Required programs
The python interpreter version 3.7 64-bit and Matlab release R2019a is needed to run the program and install required libraries. 

The 64-bit python interpreter is required for everything to work, a 32-bit version will not work. 

## Libraries
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
