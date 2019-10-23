% Functions: To embed buyer and seller watermark into an image using DCT implementation
% Parameters:
% - bWatermarkFile   - File containing buyer watermark
% - sWatermarkFile   - File containing seller watermark
% - oriImgFile       - Name of the original image file
% - wImgName         - Name for the watermarked image
% Return: A watermarked image with buyer and seller watermark
function dataEmbeddingDCT(bWatermarkFile,sWatermarkFile,oriImgFile,wImgName)
    % Opens an existing file that contains watermark of buyer (bWatermarkFile) for reading purposes
    bWatermarkF = fopen(bWatermarkFile,'r');
    % Read the data from the open text file which contains the watermark of buyer (bWatermarkF) and store it in bWatermark variable (string format)
    bWatermark = fscanf(bWatermarkF, '%s');
    % BinaryStringBuyer contains the watermark of the buyer from bWatermark
    binaryStringBuyer = bWatermark;
    % Contains the length of the buyer watermark
    lengthBinaryStringBuyer = length(binaryStringBuyer);

    % Opens an existing file that contains watermark of seller (sWatermarkFile) for reading purposes
    sWatermarkF = fopen(sWatermarkFile,'r');
    % Read the data from the open text file which contains the watermark of seller (sWatermarkF) and store it in sWatermark variable (string format)
    sWatermark = fscanf(sWatermarkF, '%s');
    % BinaryStringSeller contains the watermark of the seller from sWatermark
    binaryStringSeller = sWatermark;
    % Contains the length of the seller watermark
    lengthBinaryStringSeller = length(binaryStringSeller);

    % Reads the image from oriImgFile and store it in image
    image = imread(oriImgFile);
    % Store the sizes of each dimension of the image
    [x,y,z] = size(image);
    % Converting the image from rgb color to ycbcr color and store it in ycbcr
    ycbcr = rgb2ycbcr(image);
    % Use dct2 function to obtain the dct coefficient based on the luminance of the image
    DCTCOE = dct2(ycbcr(:,:,1));
    % Store the width and height of the image into img_size_w and img_size_h
    [img_size_w, img_size_h] = size(DCTCOE);

    % block_size is the size of the block where we store our watermark and it is hardcoded
    block_size = 12;
    % blockPixels is the 2D size of the block
    blockPixels = block_size * block_size;
    % embed_per_size is the number of block that can fit into the image for a single dimension (width)
    embed_per_size = floor(img_size_w / block_size);
    % blocksToEmbed is the total number of block that can fit into the image
    blocksToEmbed = floor((embed_per_size*embed_per_size)/2);
    % max_embed_times_Buyer is the maximum number of times that the buyer watermark can be embedded into the image
    max_embed_times_Buyer = floor((blocksToEmbed*blockPixels)/lengthBinaryStringBuyer);
    % max_embed_times_Seller is the maximum number of times that the seller watermark can be embedded into the image
    max_embed_times_Seller = floor((blocksToEmbed*blockPixels)/lengthBinaryStringSeller);

    % blockRow indicates the row of the block
    blockRow = 1;
    % blockCol indicates the column of the block
    blockCol = 1;
    % sp_row indicates the starting position of the row
    sp_row = 1;
    % ep_row indicates the ending position of the row
    ep_row = block_size;
    % sp_col indicates the starting position of the col
    sp_col = 1;
    % ep_col indicates the ending position of the col
    ep_col = block_size;

    % index of the current character for buyer watermark
    index_Buyer_Watermark = 1;

    % times_embed keep tracks of the number of times that the watermark is embedded
    times_embed = 0;

    % isNegative is a flag that indicates whether the value in the current position of the dct coefficient is a negative (isNegative == 0) or positive (isNegative == 1) value
    isNegative = -1;

    % Buyer watermark will be embedded with max_embed_times_Buyer number of times
    while times_embed < max_embed_times_Buyer
        sp_row = blockRow;
        ep_row = blockRow + block_size - 1;
        sp_col = blockCol;
        ep_col = blockCol + block_size - 1;

        % Handling the case if the starting row or col or ending row or col has exceeded the size of the image
        if (sp_row>img_size_w||ep_row>img_size_w||sp_col>img_size_h||ep_col>img_size_h)
            break;
        end

        % Iterating through the row of the image
        for i = sp_row:ep_row
            % If the index of that points to the character in the buyer watermark has exceed the length of the buyer watermark
            if index_Buyer_Watermark > lengthBinaryStringBuyer
                % Increment the number of times the watermark has been embedded by 1
                times_embed = times_embed + 1;
                % Change the index pointer to the first character in the buyer watermark
                index_Buyer_Watermark = 1;
            end

            % Iterating through the column of the image
            for j = sp_col:ep_col
                % If the index of that points to the character in the buyer watermark has exceed the length of the buyer watermark
                if index_Buyer_Watermark > lengthBinaryStringBuyer
                    % Increment the number of times the watermark has been embedded by 1
                    times_embed = times_embed + 1;
                    % Change the index pointer to the next character in the buyer watermark
                    index_Buyer_Watermark = 1;
                end

                % Determine whether the current position of the DCT coefficient is a negative or positive number
                if DCTCOE(i,j) >= 0
                    % floor function is used to convert the value in the current position of the dct coefficient to an integer value
                    % It is then stored in currentDCTValue
                    currentDCTValue = floor(DCTCOE(i,j));
                    isNegative = 0;
                else
                    % ceil function is used to convert the value in the current position of the dct coefficient to an integer value
                    % It is then stored in currentDCTValue
                    currentDCTValue = ceil(DCTCOE(i,j));
                    isNegative = 1;
                end

                % Converts currentDCTValue from numeric to string and stored it in currentDCTValue_str
                currentDCTValue_str = num2str(currentDCTValue);
                % Getting the right most digit of the currentDCTValue_str and stored it in rmost_digit
                rmost_digit = extractAfter(currentDCTValue_str, length(currentDCTValue_str)-1);
                % Converts rmost_digit from string to double
                rmost_digit = str2double(rmost_digit);

                % Check if the the current index of the character in buyer watermark == 49 (1)
                if binaryStringBuyer(index_Buyer_Watermark) == 49
                    % Check if the value in the current position of the dct coefficient is negative
                    if isNegative == 0
                        diff = rmost_digit - 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                % Check if the the current index of the character in buyer watermark == 48 (0)
                elseif binaryStringBuyer(index_Buyer_Watermark) == 48
                    % Check if the value in the current position of the dct coefficient is negative
                    if isNegative == 0
                        diff = rmost_digit - 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                end

                index_Buyer_Watermark = index_Buyer_Watermark + 1;
            end
        end

        blockCol = blockCol + block_size;
        % Check if the current column of the block is reaching the end of the block
        if mod(blockCol, block_size*embed_per_size) == 1
            % Switch to next row of the block
           blockRow = blockRow + block_size; 
        end
        % Switch to next column of the block
        blockCol = mod(blockCol, block_size*embed_per_size);
    end

    % Similar to the code above
    % Only difference is that this code does watermark embedding for the seller watermark using DCT
    index_Seller_Watermark = 1;
    times_embed = 0;
    while times_embed < max_embed_times_Seller
        sp_row = blockRow;
        ep_row = blockRow + block_size - 1;
        sp_col = blockCol;
        ep_col = blockCol + block_size - 1;
        if (sp_row>img_size_w||ep_row>img_size_w||sp_col>img_size_h||ep_col>img_size_h)
            break;
        end

        for i = sp_row:ep_row
            if index_Seller_Watermark > lengthBinaryStringSeller
                times_embed = times_embed + 1;
                index_Seller_Watermark = 1;
            end
            for j = sp_col:ep_col
                if index_Seller_Watermark > lengthBinaryStringSeller
                    times_embed = times_embed + 1;
                    index_Seller_Watermark = 1;
                end

                if DCTCOE(i,j) >= 0
                    currentDCTValue = floor(DCTCOE(i,j));
                    isNegative = 0;
                else
                    currentDCTValue = ceil(DCTCOE(i,j));
                    isNegative = 1;
                end
                currentDCTValue_str = num2str(currentDCTValue);
                rmost_digit = extractAfter(currentDCTValue_str, length(currentDCTValue_str)-1);
                rmost_digit = str2double(rmost_digit);

                if binaryStringSeller(index_Seller_Watermark) == 49
                    if isNegative == 0
                        diff = rmost_digit - 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                elseif binaryStringSeller(index_Seller_Watermark) == 48
                    if isNegative == 0
                        diff = rmost_digit - 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                end

                index_Seller_Watermark = index_Seller_Watermark + 1;
            end
        end

        blockCol = blockCol + block_size;
        if mod(blockCol, block_size*embed_per_size) == 1
           blockRow = blockRow + block_size; 
        end
        blockCol = mod(blockCol, block_size*embed_per_size);
    end

    % Inverse dct function is used on the coefficient of the DCT that our code has modified
    % Is then converts into unit8 format and stored into the luminance of the image
    ycbcr(:,:,1) = uint8(idct2(DCTCOE));

    % Create another image following the wImgName given by the user
    % This newly created image contains both watermarks of buyer and seller in the image
    imwrite(ycbcr2rgb(ycbcr), wImgName,'jpg','Quality',100);