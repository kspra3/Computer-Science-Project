% Functions: To extract buyer and seller watermark from a watermarked image
% Parameters:
% - bWatermarkFile   - File containing buyer watermark
% - sWatermarkFile   - File containing seller watermark
% - wImgName         - Name of the watermarked image
% Return: two files each containing the extracted watermark of either buyer or seller
function dataExtractingDCT(bWatermarkFile,sWatermarkFile,wImgName)
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

    % Reads the image from wImgName and store it in image
    image = imread(wImgName);
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
    % max_embed_times_Buyer is the maximum number of times that the buyer watermark is embedded into the image
    max_embed_times_Buyer = floor((blocksToEmbed*blockPixels)/lengthBinaryStringBuyer);
    % max_embed_times_Seller is the maximum number of times that the seller watermark is embedded into the image
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

    % Create an array containing 0 that has the size of the buyer watermark
    bin_1_array_Buyer = zeros(lengthBinaryStringBuyer);
    bin_0_array_Buyer = zeros(lengthBinaryStringBuyer);

    % times_embed keep tracks of the number of times that the watermark is extracted
    times_embed = 0;

    % isNegative is a flag that indicates whether the value in the current position of the dct coefficient is a negative (isNegative == 0) or positive (isNegative == 1) value
    isNegative = -1;

    % Buyer watermark will be extracted with max_embed_times_Buyer number of times
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
            % Check if the index of that points to the character in the buyer watermark has exceed the length of the buyer watermark
            if index_Buyer_Watermark > lengthBinaryStringBuyer
                % Increment the number of times the watermark has been extracted by 1
                times_embed = times_embed + 1;
                % Change the index pointer to the first character in the buyer watermark
                index_Buyer_Watermark = 1;
            end

            % Iterating through the column of the image
            for j = sp_col:ep_col
                % Check if the index of that points to the character in the buyer watermark has exceed the length of the buyer watermark
                if index_Buyer_Watermark > lengthBinaryStringBuyer
                    % Increment the number of times the watermark has been extracted by 1
                    times_embed = times_embed + 1;
                    % Change the index pointer to the first character in the buyer watermark
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

                % Check if the right most digit falls within the range of 0 ~ 4 and 5 ~ 9
                if (0 <= rmost_digit) && (rmost_digit <= 4)
                    % Counter for 0 is incremented by 1 at the current position
                    bin_0_array_Buyer(index_Buyer_Watermark) = bin_0_array_Buyer(index_Buyer_Watermark) + 1;
                else
                    % Counter for 1 is incremented by 1 at the current position
                    bin_1_array_Buyer(index_Buyer_Watermark) = bin_1_array_Buyer(index_Buyer_Watermark) + 1;
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

    % Creating binary string
    out_bstr_Buyer = '';
    for i = 1:lengthBinaryStringBuyer
        one_count = bin_1_array_Buyer(i);
        zero_count = bin_0_array_Buyer(i);

        % Check if occurrence of 1 is greater than occurrence of 0
        if one_count > zero_count
            out_bstr_Buyer = append(out_bstr_Buyer,'1');
        else
            out_bstr_Buyer = append(out_bstr_Buyer,'0');
        end
    end

    % Write the extracted buyer watermark into a file
    buyerExtractedFile = strcat("extracted_", bWatermarkFile);
    extractedBuyerInfoF = fopen(buyerExtractedFile, 'w');
    fprintf(extractedBuyerInfoF,"%s",out_bstr_Buyer);
    
    % Similar to the code above
    % Only difference is that this code extracts seller watermark
    index_Seller_Watermark = 1;
    bin_1_array_Seller = zeros(lengthBinaryStringSeller);
    bin_0_array_Seller = zeros(lengthBinaryStringSeller);
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

                if (0 <= rmost_digit) && (rmost_digit <= 4)
                    % 0 is encoded
                    bin_0_array_Seller(index_Seller_Watermark) = bin_0_array_Seller(index_Seller_Watermark) + 1;
                else
                    % 1 is encoded
                    bin_1_array_Seller(index_Seller_Watermark) = bin_1_array_Seller(index_Seller_Watermark) + 1;
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

    % Creating binary string
    out_bstr_Seller = '';
    for i = 1:lengthBinaryStringSeller
        one_count = bin_1_array_Seller(i);
        zero_count = bin_0_array_Seller(i);

        if one_count > zero_count
            out_bstr_Seller = append(out_bstr_Seller,'1');
        else
            out_bstr_Seller = append(out_bstr_Seller,'0');
        end
    end

    sellerExtractedFile = strcat("extracted_", sWatermarkFile);
    extractedSellerInfoF = fopen(sellerExtractedFile, 'w');
    fprintf(extractedSellerInfoF,"%s",out_bstr_Seller);