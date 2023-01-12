img=imread("1.jpg");

figure

img2 = rot90 (img);
I = rgb2gray(img2); % image en noir et blanc

% gmag = imgradient(I);
% title('Gradient Magnitude')

se = strel('disk',20);
Ie = imerode(I,se);
Iobr = imreconstruct(Ie,I);
title('Opening-by-Reconstruction')

Iobrd = imdilate(Iobr,se);
Iobrcbr = imreconstruct(imcomplement(Iobrd),imcomplement(Iobr));
Iobrcbr = imcomplement(Iobrcbr);
title('Opening-Closing by Reconstruction')

bw = imbinarize(Iobrcbr);
imshow(bw)
title('Thresholded Opening-Closing by Reconstruction')

hold on
stats = regionprops (bw, "BoundingBox", 'Centroid')
cent = cat(1,stats.Centroid)
plot(cent(:,1), cent(:,2),'b*')
hold off
