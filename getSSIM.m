function ssimval = getSSIM(referenceImg, newImg)
    refImg = imread(referenceImg);
    nImg = imread(newImg);
    
    [ssimval,~] = ssim(nImg,refImg);
end