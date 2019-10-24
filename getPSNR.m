% Functions: To calculate the similarity between two images in terms of peak signal-to-noise ratio
% Parameters:
% - referenceImg    - Name of the first image (original image)
% - newImg          - Name of the second image (watermarked image)
% Return: The peak signal-to-noise ratio between the two images
function peaksnr = getPSNR(referenceImg, newImg)
    % Reads the image from referenceImg and store it in refImg
    refImg = imread(referenceImg);
    % Reads the image from newImg and store it in nImg
    nImg = imread(newImg);

    % calculates the peak signal-to-noise ratio for the image
    [peaksnr, ~] = psnr(nImg, refImg);
end