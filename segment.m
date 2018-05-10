function [] = segment(id,k)
    orifile = [id '.tif-new.tif'];
    command=['vips VipsResize ' orifile ' resized.tif 0.05'];
    system(command);
    filename= 'resized.tif';
    a=imread(filename);
    mask = zeros(size(a));
    b=~imbinarize(rgb2gray(a));
    se = strel('disk',5);%½á¹¹ÔªËØse

    BW2 = imdilate(b,se);
    BW2 = bwareafilt(BW2,5);
     [ height, width ] = size(a);
    BW2 = gpuArray(BW2);
    stats = regionprops('table',BW2,'BoundingBox','Area','Centroid','FilledImage');
    [~,ML] = max(stats.Area);
    stats.Area(ML)=0; 
    [~,ML] = max(stats.Area);
    disp(ML);
    
    %size(mask(578:577+111,129:128+80,:))
    %size(stats.FilledImage{1})
    box = stats.BoundingBox(ML,:);
    sf = size(stats.FilledImage{ML});
    for i = 1:3
        mask(box(2):box(2)+box(4)-1,box(1):box(1)+box(3)-1,i) = stats.FilledImage{ML};
    end
    imwrite(mask,'mask.jpg');
    for i = 1:size(mask,1)
       for j = 1: size(mask,2)
          if mask(i,j,1) > 0.98
              mask(i,j,:) = [0.06,0.06,0.06]';
          end
       end
    end
    imwrite(mask,'bimg.jpg');
    stats
    %imshow(stats.FilledImage);
    
%     if sqrt(sum((stats.Centroid(ML,:)-[height/2, width/2]).^2))> 1500
%        stats.Area(ML)=0; 
%        [~,ML] = max(stats.Area);
%        disp('second big');
%        disp(sqrt(sum((stats.Centroid(ML,:)-[height/2, width/2]).^2)));
%     end
%     if nargin == 2
%        ML = k; 
%     end
%     box = 8.*stats.BoundingBox(ML,:);
%     command=['E:\VIPS\bin\vips VipsExtractArea ' num2str(id) '_x20_z0.tif ./crop/' num2str(id) '.tif ' ...
%         num2str(box(1)-100) ' ' num2str(box(2)-100) ' ' ...
%         num2str(box(3)+200) ' ' num2str(box(4)+200)];
%     system(command);
%     command=['E:\VIPS\bin\vips VipsForeignSaveTiffFile ./crop/' num2str(id) '.tif ./crop_2/' num2str(id) '.tif --compression jpeg'];
%     system(command);
    command=['vips VipsResize mask.jpg vmask.jpg 20']
    system(command);
    command=['vips VipsResize bimg.jpg vbimg.jpg 20']
    system(command);
    command=['vips VipsBoolean ' orifile ' vmask.jpg hello-a.tif or']
    system(command);
    command=['vips VipsBoolean hello-a.tif vbimg.jpg hello.tif eor']
    system(command);
    command=['vips VipsForeignSaveTiffFile hello.tif ' orifile ' --compression deflate --predictor horizontal']
    system(command);
end

function [ img ] = median_filter( image, n )
    [ height, width ] = size(image);
    x1 = image;
    x2 = x1;
    for i = 1: height-n+1
        for j = 1:width-n+1
            mb = x1( i:(i+n-1),  j:(j+n-1) );
            mb = mb(:);
            mm = median(mb);
            x2( i+(n-1)/2,  j+(n-1)/2 ) = mm;
        end
    end
    img = x2;
end