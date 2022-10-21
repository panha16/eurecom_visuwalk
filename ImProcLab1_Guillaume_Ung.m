
%Squares
img = imread('lena.tif');
gray=rgb2gray(img);
scaleImg=imresize(gray,[128 128]);
square1=uint8(32*ones(1024,1024));
square2=uint8(64*ones(512,512));
square3=uint8(128*ones(256,256));       %creating each gray block
square1(265:776,265:776)=square2;       
square1(384:639,384:639)=square3;       %adding each gray block to the big black one
square1(448:575,448:575)=scaleImg;      %adding lena in the middle of everything

    
%Mosaic with each color channel
empty = uint8(zeros(size(img,1),size(img,2)));
R = fliplr(cat(3,img(:,:,1),empty,empty));
G = fliplr(flipud(cat(3,empty,img(:,:,2),empty)));
B = flipud(cat(3,empty,empty,img(:,:,3)));      %reading each image in its colour and flipping them
bl = uint8(zeros(1024,1024,3))                  %creating a blank image
bl(1:512,1:512,:)=img;
bl(513:1024,1:512,:)=R;
bl(513:1024,513:1024,:)=G;
bl(1:512,513:1024,:)=B;                         %adding each lena image in the blank image


%3D image
img2 = imresize(img,[256 256]);
gray2=rgb2gray(img2);                           %computing the gray level of the resized lena image
s = surf(gray2)                                 %creating the surface from the grayscale levels
set(s,'Linestyle','none ')
colormap ('gray(256)')


%Bitplane slicing
dbl = double(gray);                             %converting the pixel values to double, otherwise the division (by 2,4,8 etc) will cause problems
c0 = mod(floor(dbl),2);                         %creating each bitplane
c1 = mod(floor(dbl/2),2);
c2 = mod(floor(dbl/4),2);
c3 = mod(floor(dbl/8),2);
c4 = mod(floor(dbl/16),2);
c5 = mod(floor(dbl/32),2);
c6 = mod(floor(dbl/64),2);
c7 = mod(floor(dbl/128),2);

blank = double(zeros(1024,2048));               %creating the mosaic
blank(1:512,1:512,:) = c0
blank(1:512,513:1024,:)=c1
blank(1:512,1025:1025+511,:)= c2
blank (1:512,1025 + 512:2048,:)=c3
blank(513:1024,1:512,:)=c4
blank(513:1024,513:1024,:)=c5
blank(513:1024,1025:1025+511,:)=c6
blank(513:1024,1025+512:2048,:)=c7

