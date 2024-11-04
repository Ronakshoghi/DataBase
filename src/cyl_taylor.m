function data_cyl = cyl_taylor(name, cs, ori, cp_sim_data, path_tf, path_db, path_angles)
% NOTE: This function is using only two stress states from CPFEM or CPFFT!!
tic;
cs = crystalSymmetry(cs);
S3G = equispacedSO3Grid(cs,'resolution',2.5*degree);
filename = name;
ori = orientation('Euler',ori(:,1), ori(:,2), ori(:,3), cs);
t = importdata([path_tf]);

N = size(t,2);
theta_o = 0:2*pi/N:(2*pi-2*pi/N);
a = ones(length(theta_o),3);
a(:,1) = 1/sqrt(1.5);
a(:,2) = -0.5/sqrt(1.5);
a(:,3) = -0.5/sqrt(1.5);
b = ones(length(theta_o),3);
b(:,1) = 0*sqrt(2);
b(:,2) = 0.5*sqrt(2);
b(:,3) = -0.5*sqrt(2);
uu = cross(a(1,:),b(1,:));
strain = a.*repmat(cos(theta_o(:)),1,3)+b.*repmat(sin(theta_o(:)),1,3); 
%phase = 120*pi/180;
phase = 0;

simdata = cp_sim_data;

[~,loc] = sort(simdata(:,1));
simdata = simdata(loc,:);
simdata = abs(simdata);%I had problems with negative angles from cyl conversion.
%I don't interpolate but directly take the 60, 90 deg loadcases from CPFEM
%sel = [60,90].*pi/180;
%f =  fit(simdata(:,1),simdata(:,2),'cubicinterp'); 
%sim = [sel(:),f(sel(:))];
sim = simdata(:,1:2);

hstep = 1;
eg = [];
gflag=1;
lr = 10;
eold = 100;
theta = [];

for hw=5:hstep:45

    odf = calcKernelODF(ori,'halfwidth',hw*degree);

    val = eval(odf,S3G,'silent');
    val = val ./ sum(val);
    val = val(:);

    val = repmat(val,1,size(t,2));
    M = val.*t;
    Mm = sum(M,1);

    coord = [];

    for j=1:2:length(Mm)

        mat = [strain(j,:);strain(j+1,:);1 1 1];
        coord = [coord;...
            ((inv([strain(j,:);strain(j+1,:);1 1 1]))*[Mm(j);Mm(j+1);1])'];       

    end 

    hyd = sum(coord,2)./3;
    dev = coord - repmat(hyd,1,size(coord,2));
    % 
    mag = sqrt(dev(:,1).^2 + dev(:,2).^2 + dev(:,3).^2);

    r = sqrt(1.5).*mag;
    % 
    ndev = dev;

    ndev(:,1)=ndev(:,1)./mag;
    ndev(:,2)=ndev(:,2)./mag;
    ndev(:,3)=ndev(:,3)./mag;

    vec1 = sum(ndev.*a(1:length(dev),:),2);
    vec2 = sum(ndev.*b(1:length(dev),:),2);

    theta = atan2(vec2,vec1);

    theta(theta<0) = theta(theta<0)+2*pi;
    theta(theta>2*pi) = theta(theta>2*pi)-2*pi;


    %%%%%%%%%%%%%%%%%% rotate dev stress

    rot=zeros(3,3);

    rot(1,1) = cos(phase)+(uu(1)^2)*(1-cos(phase));
    rot(1,2) = uu(1)*uu(2)*(1-cos(phase))-uu(3)*sin(phase);
    rot(1,3) = uu(1)*uu(3)*(1-cos(phase))+uu(2)*sin(phase);

    rot(2,1) = uu(1)*uu(2)*(1-cos(phase))+uu(3)*sin(phase);
    rot(2,2) = cos(phase)+(uu(2)^2)*(1-cos(phase));
    rot(2,3) = uu(3)*uu(2)*(1-cos(phase))-uu(1)*sin(phase);

    rot(3,1) = uu(1)*uu(3)*(1-cos(phase))-uu(2)*sin(phase);
    rot(3,2) = uu(3)*uu(2)*(1-cos(phase))+uu(1)*sin(phase);
    rot(3,3) = cos(phase)+(uu(3)^2)*(1-cos(phase));

    %%%%% rotatate dev vector

    dev = [sum(repmat(rot(1,:),length(dev),1).*dev,2),...
           sum(repmat(rot(2,:),length(dev),1).*dev,2),...    
           sum(repmat(rot(3,:),length(dev),1).*dev,2)];

    mag = sqrt(dev(:,1).^2 + dev(:,2).^2 + dev(:,3).^2);

    r = sqrt(1.5).*mag;


    %%%%%%%%%%%%%%%%%%%%%

    ndev = dev;

    ndev(:,1)=ndev(:,1)./mag;
    ndev(:,2)=ndev(:,2)./mag;
    ndev(:,3)=ndev(:,3)./mag;

    vec1 = sum(ndev.*a(1:length(dev),:),2);
    vec2 = sum(ndev.*b(1:length(dev),:),2);

    theta = atan2(vec2,vec1);

    theta(theta<0) = theta(theta<0)+2*pi;
    theta(theta>2*pi) = theta(theta>2*pi)-2*pi;

    %%%%%%%%%%%%%%%%%%%%%%%%


    f = fit(theta,r,'cubicinterp'); 
    yy = f(sim(:,1));
    fac = mean(sim(:,2))/mean(yy);
    e = sum(abs(yy.*fac - sim(:,2))./(sim(:,2)));

    if min(e)<eold
        eold = e;
        devf = dev;
        hwf = hw;
        thetaf = theta;
        h = fac;    
        count = 0;
    end    

    if hw-hwf>lr
        break
    end

end
toc;
devf = devf.*h;

[~,loc] = sort(thetaf);
thetaf = thetaf(loc);
devf = devf(loc,:);

r = sqrt(1.5.*(devf(:,1).^2 + devf(:,2).^2 + devf(:,3).^2));

ttt = 0 : .01 : 2 * pi;
P = polar(ttt, 60 .* ones(size(ttt)));
set(P, 'Visible', 'off')

hold on

p1 = polar(thetaf,r,'r');
p1.LineWidth = 2.5;

p3 = polar(sim(:,1),sim(:,2),'bo');
p3.MarkerSize=10;


set(gcf,'PaperPositionMode','auto')
set(findall(gcf,'-property','FontSize'),'FontSize',15)

print('YL_comp','-dpng','-r200')

a_vec = a(1,:);
b_vec = b(1,:);
f = fit(thetaf,r,'cubicinterp'); 
%ang = [0:1:179]'*pi/180;
ang = readmatrix(path_angles);
syc = feval(f, ang);
syld =(kron(cos(ang),a_vec)+kron(sin(ang),b_vec)).*(sqrt(2/3)*syc);
mee = mean((abs(f(simdata(:,1))-simdata(:,2)))./simdata(:,2));
maa = max((abs(f(simdata(:,1))-simdata(:,2)))./simdata(:,2));
data_cyl = [round(syld,4),zeros(size(syld)), round(ang,4)];
head = ["S11","S22","S33","S12","S13","S23","theta"]';
data_cyl_table = array2table(data_cyl, 'VariableNames', head);
path_db
file_name = sprintf('CYLOutfile_%s.csv', filename);
writetable(data_cyl_table, fullfile(path_db, file_name),'Delimiter',';');
% Difference between eold and mee is that eold is the sum of all errors
