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

For more information on installing the matlab.engine package, visit [here](https://au.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html).

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