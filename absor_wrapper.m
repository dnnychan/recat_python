% Copy either of the following to run
%/Applications/MATLAB_R2013a.app/bin/matlab -nojvm -nodisplay -nosplash -r "absor_wrapper"
% matlab -nojvm -nodisplay -nosplash -r "absor_wrapper"

abs = textread('abs_coordinates.txt')';
ct = textread('ct_coordinates.txt')';

% ct_file = fopen('ct_coordinates (2).txt');
% A = fread(ct_file,[3 3],'double',1)

results = absor(ct,abs);

fileID = fopen('tf_matrix.txt','w');
fprintf(fileID,'%6.6f %6.6f %6.6f %6.6f\r\n',results.M');
fclose(fileID);

quit