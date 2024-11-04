%Plot the KDE in the FZ
cs = crystalSymmetry("432"); 
ss = specimenSymmetry("222");
ori = [0.26179938779914935, 1.340481119668881, 0.7853981633974483];
ori = orientation.byEuler(ori, cs, ss); 
hw = 5*degree;
odf = calcKernelODF(ori,'halfwidth',hw);

% Create Grid and Plot
[points_boundary, points_inner] = discretize_fz_cubicortho(5*degree); 

figure;
plot3d(odf)
hold on
xlim([0 90])
ylim([45 90])
zlim([0 45])

% xlabel('phi_1')
% ylabel('Phi')
% zlabel('phi_2')
% title(sprintf('Cubic-Orthorhombic FZ - %.1f° resolution',resolution))
scatter3(points_boundary(:,1)/degree, points_boundary(:,2)/degree, ...
    points_boundary(:,3)/degree, 50, "filled" , 'MarkerFaceColor', "#1f77b4");
scatter3(points_inner(:,1)/degree, points_inner(:,2)/degree, ...
    points_inner(:,3)/degree, 50, "filled", 'MarkerFaceColor',"#ff7f0e");


% Plot Texture Hull
boundary_ori = orientation.byEuler(points_boundary, cs, ss);
inner_ori = orientation.byEuler(points_inner, cs, ss);
ori_total = cat(1, boundary_ori, inner_ori);
texture_dir = '/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/01_TextureFiles/KDEApproach_5deg/';

% Define weight vector
alpha = zeros(size(boundary_ori));
alpha(1) = 0.5;
alpha(11) = 0.5;

alpha_inner = zeros(size(inner_ori));
alpha_inner(1) = 1;

alpha_total = zeros(size(ori_total));
alpha_total(1) = 1;


% Define an example GSH ODF (to use its functions later)
odf_gsh = SO3FunGSH(alpha, boundary_ori, 12, cs, ss);
odf_gsh_inner = SO3FunGSH(alpha_inner, inner_ori, 12, cs, ss);
odf_gsh_total = SO3FunGSH(alpha_total, ori_total, 12, cs, ss);

% Load Texture Files
texture_files = dir(strcat(texture_dir,'texturefile_*.json'));
texture_files_struct = struct2table(texture_files).name;
gsh_original = zeros(38,length(texture_files_struct));
gsh_reconstructed = zeros(38,length(texture_files_struct));
gsh_random = zeros(38,length(texture_files_struct));
errs_reconstruction = [];
errs_random = [];
oris_random = [];
oris_reconstruction = [];
hws_reconstruction = [];
central_oris = [];
hws_original = [];


for idx_texture = 1:1:length(texture_files_struct)
    fname = strcat(texture_dir,texture_files_struct{idx_texture});
    fid = fopen(fname);
    raw = fread(fid,inf);
    str = char(raw');
    fclose(fid);
    val = jsondecode(str);
    gsh_original(:,idx_texture) = val.gsh_coeff_original;
    gsh_reconstructed(:,idx_texture) = val.gsh_coeff_reconstructed_random;
    
end

gsh_reconstructed = gsh_reconstructed.';
figure
% plot3(real(odf_gsh_total.gsh_coeff_single_crystals(2,:)), ...
%     real(odf_gsh_total.gsh_coeff_single_crystals(3,:)), ...
%     real(odf_gsh_total.gsh_coeff_single_crystals(4,:)),...
%     '-o','Color','b','MarkerSize',5,'MarkerFaceColor','#D9FFFF');
figure
hold on
scatter3(gsh_reconstructed(:,2)/1, gsh_reconstructed(:,3)/1,...
    gsh_reconstructed(:,4),  10, 'filled', 'MarkerFaceColor','#2ca02c');

scatter3(real(odf_gsh_inner.gsh_coeff_single_crystals(2,:)), ...
    real(odf_gsh_inner.gsh_coeff_single_crystals(3,:)), ...
    real(odf_gsh_inner.gsh_coeff_single_crystals(4,:)),...
    20,'filled','MarkerFaceColor','#ff7f0e');

scatter3(real(odf_gsh.gsh_coeff_single_crystals(2,:)), ...
    real(odf_gsh.gsh_coeff_single_crystals(3,:)), ...
    real(odf_gsh.gsh_coeff_single_crystals(4,:)),...
    20,'filled','MarkerFaceColor','#1f77b4');

xlabel('$F_4^{1 1}$','Interpreter','latex') 
ylabel('$F_4^{2 1}$','Interpreter','latex') 
zlabel('$F_4^{3 1}$','Interpreter','latex')
% legend([p4 p2 p1],{'single crystals at boundary of fundamental zone',...
%     'single crystals inside fundamental zone',...
%     'polycrystal by increasing kernel halfwidth'}, 'Location', 'best')
% legend([p4 p2],{'single crystals at boundary of fundamental zone',...
%     'single crystals inside fundamental zone'}, 'Location', 'best')
grid on


