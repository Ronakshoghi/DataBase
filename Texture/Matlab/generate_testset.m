% Generate TextureFile.json for Test Set
% Prominent ideal components:
% - Brass, Copper, Goss
% Fibre textures
% - alpha, gamma, teta
clear all, clc
cs = crystalSymmetry("432");
ss = specimenSymmetry('222');
hw = 12*degree;
texture_dir = '/Users/jan/Documents/Promotion/04_GeorgiaTech/06_DataBase/01_TextureFiles/TestSet/';
n_grains = 1331;

% Defining orientations
ori_brass = orientation.brass(cs, ss);
ori_copper = orientation.copper(cs, ss);
ori_goss = orientation.goss(cs,ss);
f_alpha = fibre.alpha(cs, ss);
f_gamma = fibre.gamma(cs, ss);
f_theta = fibre.theta(cs, ss);

% Creating ODFs
odf_brass = calcKernelODF(ori_brass,'halfwidth',hw);
odf_copper = calcKernelODF(ori_copper,'halfwidth',hw);
odf_goss = calcKernelODF(ori_goss,'halfwidth',hw);
odf_alpha = fibreODF(f_alpha,'halfwidth',hw);
odf_gamma = fibreODF(f_gamma, 'halfwidth',hw);
odf_theta = fibreODF(f_theta, 'halfwidth',hw);
odfs = {odf_brass, odf_copper, odf_goss, odf_alpha, odf_gamma, odf_theta};
odf_names = ["brass", "copper", "goss", "alpha", "gamma", "theta"];

% Grids for addressvector
grid_ad_16 = equispacedSO3Grid(cs, ss, 'resolution',15*degree);
grid_ad_111  = equispacedSO3Grid(cs, ss, 'resolution',11*degree);
grid_ad_1232 = equispacedSO3Grid(cs, ss, 'resolution',5*degree);

[points_boundary, points_inner] = discretize_fz_cubicortho(5*degree);
ori_boundary = orientation.byEuler(points_boundary, cs, ss);
ori_inner = orientation.byEuler(points_inner, cs, ss);
ori_total = cat(1, ori_boundary, ori_inner);
grid_ad_1737 = ori_total; %single crystals have 0 intensity except for their central ori

%Create example gsh odf
alpha = zeros(size(ori_total));
alpha(1) = 1;
odf_gsh_total = SO3FunGSH(alpha, ori_total, 12, cs, ss);

% CREATE FILES
for idx_odf = 1:length(odfs)
    texture_struct = struct;
    odf_kde = odfs{idx_odf};
    textureindex(odf_kde)

    % Kernels for reconstruction
    psi_reduction = SO3DeLaValleePoussinKernel('halfwidth', 5*degree);
    ebsd_mock = discreteSample(odf_kde, 50000);
    ebsd_mock.SS =specimenSymmetry('1');

%     % Abhishek's Reduction
    [orired,odfred_f,err,odf] = textureReconstruction_mtex10(n_grains, ...
        'orientation', ebsd_mock, 'kernel', psi_reduction);%'odf_true', odf_kde)         
    fprintf('Texture %d. Halfwidth %5f: Error after reduction: %.5f\n', [idx_odf, hw,err]);
    ori_texture = orired.project2FundamentalRegion;

    % Alternative Way of determining the reduced orientations
    ebsd_random = discreteSample(odf_kde, n_grains);
    ebsd_random.SS =specimenSymmetry('1');
    odf_ebsd = calcKernelODF(ebsd_mock,'kernel', psi_reduction);
    odf_random = calcKernelODF(ebsd_random,'kernel', psi_reduction);
    err_random = calcError(odf_ebsd, odf_random) %This compares the same error as Abhishek
    
    ori_texture_random = ebsd_random.project2FundamentalRegion;
    norm(odf_ebsd)^2
    norm(odf_random)^2
    % Fill Struct
    texture_struct.name = odf_names(idx_odf);
    texture_struct.halfwidth = hw*degree;
    texture_struct.halfwidth_reconstructed_random = odf_ebsd.psi.halfwidth;

    % Add orientations to Struct
    texture_struct.discrete_orientations_random =[...
    ori_texture_random.phi1, ori_texture_random.Phi, ... 
    ori_texture_random.phi2];

%     texture_struct.discrete_orientations = [ori_texture.phi1', ...
%         ori_texture.Phi', ori_texture.phi2'];

    % Add GSH coeff
%     texture_struct.gsh_coeff_reconstructed = mean(real(...
%         odf_gsh_total.calc_coeff_single_crystal(ori_texture)),2);
    texture_struct.gsh_coeff_original = mean(real(...
        odf_gsh_total.calc_coeff_single_crystal(ebsd_mock)),2);
    texture_struct.gsh_coeff_reconstructed_random = mean(real(...
        odf_gsh_total.calc_coeff_single_crystal(ebsd_random)),2);

    % Add ADD Descritpor
%     texture_struct.error_reconstruction = err;
%     texture_struct.error_random = err_random;
%     texture_struct.texture_index = norm(odfred_f)^2;
%     texture_struct.address_vector_16 = eval(odfred_f, grid_ad_16);
%     texture_struct.address_vector_111 = eval(odfred_f, grid_ad_111);
%     texture_struct.address_vector_1232 = eval(odfred_f, grid_ad_1232);
%     texture_struct.address_vector_1737 = eval(odfred_f, grid_ad_1737);

    texture_struct.texture_index = norm(odf_ebsd)^2;
    texture_struct.address_vector_16 = eval(odf_ebsd, grid_ad_16);
    texture_struct.address_vector_111 = eval(odf_ebsd, grid_ad_111);
    texture_struct.address_vector_1232 = eval(odf_ebsd, grid_ad_1232);
    texture_struct.address_vector_1737 = eval(odf_ebsd, grid_ad_1737);

    % Now I can write the orientations to file
    texture_name = sprintf('texturefile_polycrystal_%s_hw_%d.json', ...
       texture_struct.name, round(hw/degree));
    json_content = jsonencode(texture_struct,PrettyPrint=true);
    fid = fopen(strcat(texture_dir,texture_name),'w');
    fprintf(fid,'%s',json_content);
    fclose(fid);
end

