% Author: Pang Xu Xuan
function dataEmbeddingDCT(bWatermarkFile,sWatermarkFile,oriImgFile,wImgName)
    bWatermarkF = fopen(bWatermarkFile,'r');
    bWatermark = fscanf(bWatermarkF, '%s');
    bstr1 = bWatermark;
    binaryString1 = strrep(bstr1,'|','');
    bstr_length1 = length(binaryString1);
    %fprintf("Length of binary code: %d \n", bstr_length1);
    sWatermarkF = fopen(sWatermarkFile,'r');
    sWatermark = fscanf(sWatermarkF, '%s');
    bstr2 = sWatermark;
    binaryString2 = strrep(bstr2,'|','');
    bstr_length2 = length(binaryString2);
    %fprintf("Length of binary code: %d \n", bstr_length2);

    image = imread(oriImgFile);
    %resizedImage = imresize(image, [1000, 1000]);
    [x,y,z] = size(image);
    ycbcr = rgb2ycbcr(image);
    DCTCOE = dct2(ycbcr(:,:,1));
    [img_size_w, img_size_h] = size(DCTCOE);
    %fprintf("img_size_w: %d, img_size_h: %d \n", img_size_w,img_size_h);
    
    block_size = 12; %Blocksize is hardcoded
    embed_per_size = floor(img_size_w / block_size);
    blocksToEmbed = floor((embed_per_size*embed_per_size)/2);
    blockPixels = block_size * block_size;
    max_embed_times1 = floor((blocksToEmbed*blockPixels)/bstr_length1);
    max_embed_times2 = floor((blocksToEmbed*blockPixels)/bstr_length2);
    %fprintf("max_embed_times1: %d, max_embed_times2: %d \n", max_embed_times1,max_embed_times2);

    % fid = fopen('LogFile2.txt', 'w');
    % if fid == -1
    %   error('Cannot open log file.');
    % end

    blockRow = 1;
    blockCol = 1;
    sp_X = 1;
    ep_X = block_size;
    sp_Y = 1;
    ep_Y = block_size;
    counter = 1;

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

                if binaryString1(counter) == 49
                    if isNegative == 0
                        diff = rmost_digit - 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                elseif binaryString1(counter) == 48
                    if isNegative == 0
                        diff = rmost_digit - 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                end
                %fprintf('Binary Code: %d .DCTCOE After: %f \n',bstr1(counter),DCTCOE(i,j));
                counter = counter + 1;

            end
        end

        blockCol = blockCol + block_size;
        if mod(blockCol, block_size*embed_per_size) == 1
           blockRow = blockRow + block_size; 
        end
        blockCol = mod(blockCol, block_size*embed_per_size);

    end

    counter = 1;
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

                if binaryString2(counter) == 49
                    if isNegative == 0
                        diff = rmost_digit - 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 7;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                elseif binaryString2(counter) == 48
                    if isNegative == 0
                        diff = rmost_digit - 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    elseif isNegative == 1
                        diff = -rmost_digit + 2;
                        DCTCOE(i,j) = DCTCOE(i,j) - diff;
                    end
                end
                %fprintf('Binary Code: %d .DCTCOE After: %f \n',binaryString2(counter),DCTCOE(i,j));
                counter = counter + 1;

            end
        end

        blockCol = blockCol + block_size;
        if mod(blockCol, block_size*embed_per_size) == 1
           blockRow = blockRow + block_size; 
        end
        blockCol = mod(blockCol, block_size*embed_per_size);

    end

    ycbcr(:,:,1) = uint8(idct2(DCTCOE));
    colorDCTCOE = dct2(ycbcr(:,:,1));
    imwrite(ycbcr2rgb(ycbcr), wImgName,'jpg','Quality',100);