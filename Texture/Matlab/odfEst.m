function [todf,hw] = odfEst(ori,w,hw,odf)

e =[];
step = 0.5*degree;
w = w(:)./sum(w);
for c =1:100
    todf = calcKernelODF(ori(:),'weights',w(:),'halfwidth',hw);
    % this enforces specimen symmetry on the ODF,NOT represented by their orientations 
    %todf.SS = specimenSymmetry("222");
    e = [e calcError(odf,todf)];
    if c>1 && e(c)>e(c-1)  
       break           
    end   
    hw = hw+step;
    
end   

hw = hw-step;
todf = calcKernelODF(ori,'weights',w,'halfwidth',hw);
% this enforces specimen symmetry on the ODF,NOT represented by their orientations 
%todf.SS = specimenSymmetry("222");


