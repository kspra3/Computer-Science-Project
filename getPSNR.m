function peaksnr = getPSNR(referenceImg, newImg)
    refImg = imread(referenceImg);
    nImg = imread(newImg);
    
    [peaksnr, ~] = psnr(nImg, refImg);
end