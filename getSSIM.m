% Functions: To calculate the similarity between two images in terms of Structural Similarity Index
% Parameters:
% - referenceImg    - Name of the first image (original image)
% - newImg          - Name of the second image (watermarked image)
% Return: The Structural Similarity Index between the two images
function ssimval = getSSIM(referenceImg, newImg)
    % Reads the image from referenceImg and store it in refImg
    refImg = imread(referenceImg);
    % Reads the image from newImg and store it in nImg
    nImg = imread(newImg);

    % computes the Structural Similarity Index (SSIM) value for the image
    [ssimval,~] = ssim(nImg,refImg);
end