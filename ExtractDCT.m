% Author: Pang Xu Xuan
function dataExtractingDCT(bWatermarkFile,sWatermarkFile,wImgName)
    bWatermarkF = fopen(bWatermarkFile,'r');
    bWatermark = fscanf(bWatermarkF, '%s');
    bstr1 = bWatermark;
    fprintf("Buyer's Watermark: %s \n",bstr1);
    binaryString1 = strrep(bstr1,'|','');
    bstr_length1 = length(binaryString1);
    %fprintf("Length of binary code: %d \n", bstr_length1);
    sWatermarkF = fopen(sWatermarkFile,'r');
    sWatermark = fscanf(sWatermarkF, '%s');
    bstr2 = sWatermark;
    fprintf("Seller's Watermark: %s \n",bstr2);
    binaryString2 = strrep(bstr2,'|','');
    bstr_length2 = length(binaryString2);
    %fprintf("Length of binary code: %d \n", bstr_length2);
    
    image = imread(wImgName);
    [x,y,z] = size(image);
    ycbcr = rgb2ycbcr(image);
    DCTCOE = dct2(ycbcr(:,:,1));
    [img_size_w, img_size_h] = size(DCTCOE);
    
    block_size = 12; %Blocksize is hardcoded
    embed_per_size = floor(img_size_w / block_size);
    blocksToEmbed = floor((embed_per_size*embed_per_size)/2);
    blockPixels = block_size * block_size;
    max_embed_times1 = floor((blocksToEmbed*blockPixels)/bstr_length1);
    max_embed_times2 = floor((blocksToEmbed*blockPixels)/bstr_length2);

    blockRow = 1;
    blockCol = 1;
    sp_X = 1;
    ep_X = block_size;
    sp_Y = 1;
    ep_Y = block_size;
    counter = 1;

    bin_1_array1 = zeros(bstr_length1);
    bin_0_array1 = zeros(bstr_length1);
    
    times_embed = 0;
    while times_embed < max_embed_times1
        %fprintf("row: %d col: %d \n", blockRow, blockCol);
        sp_X = blockRow;
        ep_X = blockRow + block_size - 1;
        sp_Y = blockCol;
        ep_Y = blockCol + block_size - 1;
        %fprintf("starting row: %d ending row: %d \n", sp_X, ep_X);
        %fprintf("starting col: %d ending col: %d \n", sp_Y, ep_Y);

        for i = sp_X:ep_X
            if counter > bstr_length1
                times_embed = times_embed + 1;
                counter = 1;
            end
            for j = sp_Y:ep_Y
                if counter > bstr_length1
                    times_embed = times_embed + 1;
                    counter = 1;
                end

                %fprintf('i: %d. j: %d. Value: %f\n',i,j,DCTCOE(i,j));
                if DCTCOE(i,j) >= 0
                    a = floor(DCTCOE(i,j));
                    isNegative = 0;
                else
                    a = ceil(DCTCOE(i,j));
                    isNegative = 1;
                end
                a_str = num2str(a);
                rmost_digit = extractAfter(a_str, length(a_str)-1);
                rmost_digit = str2double(rmost_digit);

                if (0 <= rmost_digit) && (rmost_digit <= 4)
                    % 0 is encoded
                    bin_0_array1(counter) = bin_0_array1(counter) + 1;
                else
                    % 1 is encoded
                    bin_1_array1(counter) = bin_1_array1(counter) + 1;
                end
                %fprintf('Binary Code: %d .DCTCODE After: %f \n',bstr(counter),DCTCOE(i,j));
                counter = counter + 1;

            end
        end

        blockCol = blockCol + block_size;
        if mod(blockCol, block_size*embed_per_size) == 1
           blockRow = blockRow + block_size; 
        end
        blockCol = mod(blockCol, block_size*embed_per_size);

    end

    %creating binary string
    out_bstr1 = '';  
    for i = 1:bstr_length1
        one_count = bin_1_array1(i);
        zero_count = bin_0_array1(i);

        if one_count > zero_count
            out_bstr1 = append(out_bstr1,'1');
        else
            out_bstr1 = append(out_bstr1,'0');
        end
    end
    fprintf("Extracted Buyer's Watermark: %s\n",out_bstr1);
    
    extractedBuyerInfoF = fopen('extractedBuyerInfo.txt', 'w');
    fprintf(extractedBuyerInfoF,"%s",out_bstr1);
    
    counter = 1;

    bin_1_array2 = zeros(bstr_length2);
    bin_0_array2 = zeros(bstr_length2);

    times_embed = 0;
    while times_embed < max_embed_times2
        %fprintf("row: %d col: %d \n", blockRow, blockCol);
        sp_X = blockRow;
        ep_X = blockRow + block_size - 1;
        sp_Y = blockCol;
        ep_Y = blockCol + block_size - 1;
        %fprintf("starting row: %d ending row: %d \n", sp_X, ep_X);
        %fprintf("starting col: %d ending col: %d \n", sp_Y, ep_Y);

        for i = sp_X:ep_X
            if counter > bstr_length2
                times_embed = times_embed + 1;
                counter = 1;
            end
            for j = sp_Y:ep_Y
                if counter > bstr_length2
                    times_embed = times_embed + 1;
                    counter = 1;
                end

                %fprintf('i: %d. j: %d. Value: %f\n',i,j,DCTCOE(i,j));
                if DCTCOE(i,j) >= 0
                    a = floor(DCTCOE(i,j));
                    isNegative = 0;
                else
                    a = ceil(DCTCOE(i,j));
                    isNegative = 1;
                end
                a_str = num2str(a);
                rmost_digit = extractAfter(a_str, length(a_str)-1);
                rmost_digit = str2double(rmost_digit);

                if (0 <= rmost_digit) && (rmost_digit <= 4)
                    % 0 is encoded
                    bin_0_array2(counter) = bin_0_array2(counter) + 1;
                else
                    % 1 is encoded
                    bin_1_array2(counter) = bin_1_array2(counter) + 1;
                end
                %fprintf('Binary Code: %d .DCTCODE After: %f \n',bstr(counter),DCTCOE(i,j));
                counter = counter + 1;

            end
        end

        blockCol = blockCol + block_size;
        if mod(blockCol, block_size*embed_per_size) == 1
           blockRow = blockRow + block_size; 
        end
        blockCol = mod(blockCol, block_size*embed_per_size);

    end

    %creating binary string
    out_bstr2 = '';  
    for i = 1:bstr_length2
        one_count = bin_1_array2(i);
        zero_count = bin_0_array2(i);

        if one_count > zero_count
            out_bstr2 = append(out_bstr2,'1');
        else
            out_bstr2 = append(out_bstr2,'0');
        end
    end
    fprintf("Extracted Seller's Watermark: %s\n",out_bstr2);
    
    extractedSellerInfoF = fopen('extractedSellerInfo.txt', 'w');
    fprintf(extractedSellerInfoF,"%s",out_bstr2);
    
    if out_bstr1 == bstr1
        disp("Extracted Buyer's Watermark == Embedded Buyer's Watermark")
    end
    if out_bstr2 == bstr2
        disp("Extracted Seller's Watermark == Embedded Seller's Watermark")
    end