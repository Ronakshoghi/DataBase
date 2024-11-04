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

% Grids for addressvector
grid_ad_16 = equispacedSO3Grid(cs, ss, 'resolution',15*degree);
grid_ad_111  = equispacedSO3Grid(cs, ss, 'resolution',11*degree);
grid_ad_1232 = equispacedSO3Grid(cs, ss, 'resolution',5*degree);


ori_boundary = orientation.byEuler(points_boundary, cs, ss);
ori_inner = orientation.byEuler(points_inner, cs, ss);
ori_total = cat(1, ori_boundary, ori_inner);
grid_ad_1737 = ori_total; %single crystals have 0 intensity except for their central ori

%Create example gsh odf
alpha = zeros(size(ori_total));
alpha(1) = 1;
odf_gsh_total = SO3FunGSH(alpha, ori_total, 12, cs, ss);


% Sample single orientations
psi = SO3DeLaValleePoussinKernel('halfwidth', 0.1*degree);
for ori_idx = 1:length(ori_total)
    texture_struct = struct;
    odf_kde = calcKernelODF(ori_total(ori_idx),'kernel',psi);
    ebsd_mock = discreteSample(odf_kde, n_grains);
    ebsd_mock.SS =specimenSymmetry('1');
    ori_texture = ebsd_mock.project2FundamentalRegion; %no influence on coefficients though!
    texture_struct.cenral_orientation = [ori_total(ori_idx).phi1, ...
        ori_total(ori_idx).Phi, ori_total(ori_idx).phi2];
    texture_struct.halfwidth = 0.1*degree;
    texture_struct.halfwidth_reconstructed_random = 0.1*degree;
    texture_struct.discrete_orientations_random = [ori_texture.phi1, ...
        ori_texture.Phi, ori_texture.phi2];
    texture_struct.gsh_coeff_reconstructed_random = mean(real(...
        odf_gsh_total.calc_coeff_single_crystal(ori_texture)),2);

    texture_struct.gsh_coeff_original = mean(real(...
        odf_gsh_total.calc_coeff_single_crystal(ori_total(ori_idx))),2);
    texture_struct.texture_index = norm(odf_kde)^2;
    texture_struct.address_vector_16 = eval(odf_kde, grid_ad_16);
    texture_struct.address_vector_111 = eval(odf_kde, grid_ad_111);
    texture_struct.address_vector_1232 = eval(odf_kde, grid_ad_1232);
    texture_struct.address_vector_1737 = eval(odf_kde, grid_ad_1737);

    texture_name = sprintf('texturefile_singlecrystal_%d.json', ori_idx);
    texture_struct.name = texture_name(1:end-5);
    json_content = jsonencode(texture_struct,PrettyPrint=true);
    fid = fopen(strcat(texture_dir,texture_name),'w');
    fprintf(fid,'%s',json_content);
    fclose(fid);
end
prog_distance = @(x) x^1.2;
dist = 2;
range_hw = 5;
x_new  = 0;
while x_new < 45
x_new = range_hw(end)+dist;
dist = prog_distance(dist);
range_hw = cat(1,range_hw,x_new);
end
range_hw = range_hw(1:end-1);
range_hw = cat(1,range_hw, 45);

errs_reconstruction = [];
% Create polycrystals for the boundary
for idx_hw = 1:length(range_hw)
    halfwidth = range_hw(idx_hw);
    psi = SO3DeLaValleePoussinKernel('halfwidth', halfwidth*degree);
    psi_reduction = SO3DeLaValleePoussinKernel('halfwidth', 5*degree);
    for ori_idx = 1:length(ori_boundary) 
        texture_struct = struct;
        odf_kde = calcKernelODF(ori_boundary(ori_idx),'kernel',psi);
        ebsd_mock = discreteSample(odf_kde, 50000);
        ebsd_mock.SS =specimenSymmetry('1');
%         [orired,odfred_f,err,odf] = textureReconstruction_mtex10(n_grains, ...
%             'orientation', ebsd_mock, 'kernel', psi_reduction);%'odf_true', odf_kde)
%         fprintf('Texture %d. Halfwidth %5f: Error after reduction: %.5f\n', [ori_idx, halfwidth,err]);
%         ori_texture = orired.project2FundamentalRegion;

        % Alternative Way of determining the reduced orientations
        ebsd_random = discreteSample(odf_kde, n_grains);
        ebsd_random.SS =specimenSymmetry('1');
        odf_ebsd = calcKernelODF(ebsd_mock,'kernel', psi_reduction);
        odf_random = calcKernelODF(ebsd_random,'kernel', psi_reduction);
        err_random = calcError(odf_ebsd, odf_random);
        
        ori_texture_random = ebsd_random.project2FundamentalRegion;
%         ori_texture_mock = ebsd_mock.project2FundamentalRegion;
        
        texture_struct.cenral_orientation = [ori_boundary(ori_idx).phi1, ...
            ori_boundary(ori_idx).Phi, ori_boundary(ori_idx).phi2];
        texture_struct.halfwidth = halfwidth*degree;
%         texture_struct.halfwidth_reconstructed = odfred_f.psi.halfwidth;
        texture_struct.halfwidth_reconstructed_random = odf_ebsd.psi.halfwidth;

%         texture_struct.discrete_orientations = [ori_texture.phi1', ...
%             ori_texture.Phi', ori_texture.phi2'];
        texture_struct.discrete_orientations_random =[...
        ori_texture_random.phi1, ori_texture_random.Phi, ... 
        ori_texture_random.phi2];
%         texture_struct.discrete_orientations_mock = [...
%         ori_texture_mock.phi1, ori_texture_mock.Phi, ... 
%         ori_texture_mock.phi2];

%         texture_struct.gsh_coeff_reconstructed = mean(real(...
%             odf_gsh_total.calc_coeff_single_crystal(ori_texture)),2);
        texture_struct.gsh_coeff_original = mean(real(...
            odf_gsh_total.calc_coeff_single_crystal(ebsd_mock)),2);
        texture_struct.gsh_coeff_reconstructed_random = mean(real(...
            odf_gsh_total.calc_coeff_single_crystal(ebsd_random)),2);
%         texture_struct.error_reconstruction = err;
%         texture_struct.error_random = err_random;
%         texture_struct.texture_index = norm(odfred_f)^2;
%         texture_struct.address_vector_16 = eval(odfred_f, grid_ad_16);
%         texture_struct.address_vector_111 = eval(odfred_f, grid_ad_111);
%         texture_struct.address_vector_1232 = eval(odfred_f, grid_ad_1232);
%         texture_struct.address_vector_1737 = eval(odfred_f, grid_ad_1737);

        texture_struct.texture_index = norm(odf_ebsd)^2;
        texture_struct.address_vector_16 = eval(odf_ebsd, grid_ad_16);
        texture_struct.address_vector_111 = eval(odf_ebsd, grid_ad_111);
        texture_struct.address_vector_1232 = eval(odf_ebsd, grid_ad_1232);
        texture_struct.address_vector_1737 = eval(odf_ebsd, grid_ad_1737);

       % Now I can write the orientations to file
       texture_name = sprintf('texturefile_polycrystal_%d_hw_%d.json', ...
           [ori_idx, round(halfwidth)]);
       texture_struct.name = texture_name(1:end-5);
       json_content = jsonencode(texture_struct,PrettyPrint=true);
       fid = fopen(strcat(texture_dir,texture_name),'w');
       fprintf(fid,'%s',json_content);
       fclose(fid);
       %errs_reconstruction = cat(1, errs_reconstruction, err);
    end
end


