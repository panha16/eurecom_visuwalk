vid = VideoReader('videoligne.mp4');
depVideoPlayer = vision.DeployableVideoPlayer;  
while hasFrame(vid)
frame = readFrame(vid);
gray = rgb2gray(frame);
se = strel('disk',20);
Ie = imerode(gray,se);
Iobr = imreconstruct(Ie,gray);
Iobrd = imdilate(Iobr,se);
Iobrcbr = imreconstruct(imcomplement(Iobrd),imcomplement(Iobr));
Iobrcbr = imcomplement(Iobrcbr);
bw = imbinarize(Iobrcbr);

depVideoPlayer(bw);
end