clear
for i=307:600
    i
    id = i;
    command=['E:\VIPS\bin\vips VipsForeignSaveTiffFile ./crop/' num2str(id) '.tif ./crop_2/' num2str(id) '.tif --compression jpeg'];
    system(command);
   %segment(i); 
end