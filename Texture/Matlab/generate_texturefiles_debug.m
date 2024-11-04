% This file creates .json texture files.
% The .json texture files will be read by the python script setting up the
% crystal plasticity simulation.
% The fields are:
%
clear all,clc
texture_dir = '/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/01_TextureFiles/KDEApproach_5deg/';
n_grains = 1331;
[points_boundary, points_inner] = discretize_fz_cubicortho(5*degree);
cs = crystalSymmetry("432");
ss = specimenSymmetry('222');
poles = [Miller(1,0,0,cs)];

% % Grids for addressvector
% grid_ad_16 = equispacedSO3Grid(cs, ss, 'resolution',15*degree);
% grid_ad_111  = equispacedSO3Grid(cs, ss, 'resolution',11*degree);
% grid_ad_1232 = equispacedSO3Grid(cs, ss, 'resolution',5*degree);
% 
% 
% ori_boundary = orientation.byEuler(points_boundary, cs, ss);
% ori_inner = orientation.byEuler(points_inner, cs, ss);
% ori_total = cat(1, ori_boundary, ori_inner);
% grid_ad_1737 = ori_total; %single crystals have 0 intensity except for their central ori
% 
% %Create example gsh odf
% alpha = zeros(size(ori_boundary));
% alpha(1) = 1;
% odf_gsh_boundary = SO3FunGSH(alpha, ori_boundary, 12, cs, ss);
% 
% 
% % Sample single orientations
% psi = SO3DeLaValleePoussinKernel('halfwidth', 0.1*degree);
% for ori_idx = 1:1:2%length(ori_total)
%     texture_struct = struct;
%     odf_kde = calcKernelODF(ori_total(ori_idx),'kernel',psi);
%     ebsd_mock = discreteSample(odf_kde, n_grains);
%     %ebsd_mock.SS =specimenSymmetry('1');
%     ori_texture = ebsd_mock.project2FundamentalRegion;
%     texture_struct.cenral_orientation = [ori_total(ori_idx).phi1, ...
%         ori_total(ori_idx).Phi, ori_total(ori_idx).phi2];
%     texture_struct.halfwidth = 0.1*degree;
%     texture_struct.discrete_orientations = [ori_texture.phi1, ...
%         ori_texture.Phi, ori_texture.phi2];
%     texture_struct.gsh_coeff_reconstructed = mean(real(...
%         odf_gsh_boundary.calc_coeff_single_crystal(ori_texture)),2);
% 
%     texture_struct.gsh_coeff_original = mean(real(...
%         odf_gsh_boundary.calc_coeff_single_crystal(ori_total(ori_idx))),2);
%     texture_struct.texture_index = norm(odf_kde)^2;
%     texture_struct.address_vector_16 = eval(odf_kde, grid_ad_16);
%     texture_struct.address_vector_111 = eval(odf_kde, grid_ad_111);
%     texture_struct.address_vector_1232 = eval(odf_kde, grid_ad_1232);
%     texture_struct.address_vector_1737 = eval(odf_kde, grid_ad_1737);
% 
%     json_content = jsonencode(texture_struct,PrettyPrint=true);
%     texture_name = sprintf('texturefile_singlecrystal_%d.json', ...
%         ori_idx);
%     fid = fopen(strcat(texture_dir,texture_name),'w');
%     fprintf(fid,'%s',json_content);
%     fclose(fid);
% end
% 
% errs_reconstruction = [];
% % Create polycrystals for the boundary
% for halfwidth = 5:5:10 %45
%     psi = SO3DeLaValleePoussinKernel('halfwidth', halfwidth*degree);
%     psi_reduction = SO3DeLaValleePoussinKernel('halfwidth', 5*degree);
%     for ori_idx = 1:1:2%length(ori_boundary) 
%         texture_struct = struct;
%         odf_kde = calcKernelODF(ori_boundary(ori_idx),'kernel',psi);
%         ebsd_mock = discreteSample(odf_kde, 50000);
%         %ebsd_mock.SS =specimenSymmetry('1');
%         [orired,odfred_f,err,odf] = textureReconstruction_mtex10(n_grains, ...
%             'orientation', ebsd_mock, 'kernel', psi_reduction);%'odf_true', odf_kde)
%         fprintf('Texture %d. Halfwidth %5f: Error after reduction: %.5f\n', [ori_idx, halfwidth,err]);
%         ori_texture = orired.project2FundamentalRegion;
%         texture_struct.cenral_orientation = [ori_boundary(ori_idx).phi1, ...
%             ori_boundary(ori_idx).Phi, ori_boundary(ori_idx).phi2];
%         texture_struct.halfwidth = halfwidth*degree;
%         texture_struct.discrete_orientations = [ori_texture.phi1', ...
%             ori_texture.Phi', ori_texture.phi2'];
%         texture_struct.gsh_coeff_reconstructed = mean(real(...
%             odf_gsh_boundary.calc_coeff_single_crystal(ori_texture)),2);
%         texture_struct.gsh_coeff_original = mean(real(...
%             odf_gsh_boundary.calc_coeff_single_crystal(ebsd_mock)),2);
%         texture_struct.error_reconstruction = err;
%         texture_struct.texture_index = norm(odfred_f)^2;
%         texture_struct.address_vector_16 = eval(odfred_f, grid_ad_16);
%         texture_struct.address_vector_111 = eval(odfred_f, grid_ad_111);
%         texture_struct.address_vector_1232 = eval(odfred_f, grid_ad_1232);
%         texture_struct.address_vector_1737 = eval(odfred_f, grid_ad_1737);
% 
%        % Now I can write the orientations to file
%        json_content = jsonencode(texture_struct,PrettyPrint=true);
%        texture_name = sprintf('texturefile_polycrystal_%d_hw_%d.json', ...
%            [ori_idx, halfwidth]);
%        fid = fopen(strcat(texture_dir,texture_name),'w');
%        fprintf(fid,'%s',json_content);
%        fclose(fid);
%        errs_reconstruction = cat(1, errs_reconstruction, err);
%     end
% end

%% Read the Texture Files
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
    gsh_reconstructed(:,idx_texture) = val.gsh_coeff_reconstructed;
    gsh_random(:,idx_texture) = val.gsh_coeff_random;
    errs_reconstruction = cat(1,errs_reconstruction, ...
        val.error_reconstruction);
    errs_random = cat(1,errs_random, val.error_random);
    oris_reconstruction = cat(1, oris_reconstruction, ...
        val.discrete_orientations);
    oris_random = cat(1, oris_random, val.discrete_orientations_random);
    hws_reconstruction = cat(1, hws_reconstruction, ...
        val.halfwidth_reconstructed);
    central_oris = cat(1, central_oris, val.cenral_orientation');
    hws_original = cat(1, hws_original, val.halfwidth);
    
end

[errs_reconstruction_sort, idx_sort] = sort(errs_reconstruction);
diff_gsh_random = sqrt(sum((gsh_original-gsh_random).^2,1))';
diff_gsh_reconstruction = sqrt(sum((gsh_original-gsh_reconstructed).^2,1))';


idx = idx_sort(end); %14
idx_start = (n_grains*(idx-1))+1;
idx_end = n_grains*idx;

% Create reconstructed KDE ODF
ori_recontsructed = orientation.byEuler(oris_reconstruction( ...
    idx_start:idx_end,:), cs);
psi_reconstruction = SO3DeLaValleePoussinKernel('halfwidth', ...
    hws_reconstruction(idx));
odf_kde_reconstructed = calcKernelODF(ori_recontsructed,'kernel', ...
    psi_reconstruction);

% Create original KDE ODF
psi = SO3DeLaValleePoussinKernel('halfwidth', hws_original(idx));
ori_central = orientation.byEuler(central_oris(idx,:), cs, ss);
odf_kde_original = calcKernelODF(ori_central,'kernel', psi);

% Create the EBSD ODF
ebsd_mock = discreteSample(odf_kde_original, 50000);
ebsd_mock.SS =specimenSymmetry('1');
psi_ebsd = SO3DeLaValleePoussinKernel('halfwidth', 5*degree);
odf_ebsd = calcKernelODF(ebsd_mock,'kernel', psi_ebsd);

% Random guess ODF
ori_random = orientation.byEuler(oris_random( ...
    idx_start:idx_end,:), cs);
psi_random = SO3DeLaValleePoussinKernel('halfwidth', 5*degree);
odf_random = calcKernelODF(ori_recontsructed,'kernel', ...
    psi_reconstruction);

% Plot
figure
plotPDF(odf_kde_original, poles, 'complete', 'upper');
titletext = sprintf("Original KDE with %0.2f deg halfwidth", hws_original(idx)/degree);
title(titletext)
%setColorRange([0. 1.5], 'current');
mtexColorbar 

figure
plotPDF(odf_ebsd, poles, 'complete', 'upper');
mtexColorbar
title("EBSD ODF with 50000 orientations and 5.00 deg halfwidth")

figure
plotPDF(odf_kde_reconstructed, poles, 'complete', 'upper');
hold on
plotPDF(ori_recontsructed, poles, 'MarkerSize',2, 'MarkerFaceColor', ...
    'red', 'points', 'all');
mtexColorbar
title("Reconstructed ODF with 1331 orientations")

figure
plotPDF(odf_random, poles, 'complete', 'upper');
hold on
plotPDF(ori_random, poles, 'MarkerSize',2, 'MarkerFaceColor', ...
    'red', 'points', 'all');
mtexColorbar
title("1331 orientations from origianl KDE + 5.00 deg halfwidth")

figure
[~, idx_hw] = sort(hws_original);
idx_plot = idx_hw(end-6:end);
dims = [5,6,7];
p1 = scatter3(gsh_original(dims(1),idx_plot), gsh_original(dims(2),idx_plot), ...
    gsh_original(dims(3),idx_plot), 'o');

hold on
p2 = scatter3(gsh_reconstructed(dims(1),idx_plot), gsh_reconstructed(dims(2),idx_plot), ...
    gsh_reconstructed(dims(3),idx_plot),20, 'filled');

p3 = scatter3(gsh_random(dims(1),idx_plot), gsh_random(dims(2),idx_plot), ...
    gsh_random(dims(3),idx_plot), 20, 'filled');

xlabel('$F_4^{1 1}$','Interpreter','latex') 
ylabel('$F_4^{2 1}$','Interpreter','latex') 
zlabel('$F_4^{3 1}$','Interpreter','latex')
legend([p1 p2 p3],{'original gsh coeff','reconstructed gsh coeff', ...
    'random gsh ccoeff'},'Location', 'best')
grid on

