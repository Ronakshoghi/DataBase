function [points_boundary, points_inner] = discretize_fz_cubicortho(resolution)

resolution = resolution;
fprintf('Generating grid with res %.1°', resolution/degree)

% Create naive steps of res degree
phi1 = 0:resolution:pi/2;
phi2 = 0:resolution:pi/4;
Phi_lower_func = @(phi2) acos(cos(phi2)/sqrt(1+cos(phi2)*cos(phi2)));
delta_Phi = @(low, res) acos(cos(low)-res); % low = lower bound, res=res in rad

points_boundary = [];
points_inner = [];
for v = phi2
    Phi_lower = Phi_lower_func(v);
    upper = 0;
    Phi = [Phi_lower];%before first Phi_lower was not included 
    while upper<pi/2
        upper=delta_Phi(Phi_lower, resolution);
        Phi_lower=upper;
        Phi = cat(1,Phi, Phi_lower);
    end
    Phi(end) = [];
    %Phi = Phi_lower:resolution:pi/2;
    [phi_1, Phi_] = meshgrid(phi1, Phi);
    [nRow, nCol] = size(phi_1);
    phi_1_list = reshape(phi_1, [nRow*nCol, 1]);
    Phi_list = reshape(Phi_, [nRow*nCol, 1]);

    %determine points on the boundary k
    if v == 0 || v == pi/4
        k = 1:length(phi_1_list);
    else    
        k = boundary(phi_1_list, Phi_list, 1);
    end  
    phi_1_plot = phi_1_list(k);
    Phi_plot = Phi_list(k);

    phi_1_inner = phi_1_list(setdiff(1:end,k));
    Phi_inner = Phi_list(setdiff(1:end,k));
 
    % delete interior points for Phi>60°
    % This is neccessary due to the curved boundry. Some Phi-phi1-planes
    % will have boundry points where Phi < 90 degree. We don't want to have
    % this points as they don't lie on the boundary of the FZ. We delete
    % them and create the real boundary for Phi=90 in a seperate step.
    if v > 0 && v < pi/4
        % find positions of points in phi_list that are in fundamental zone
        % but detected as boundary by matlab method boundary
        mask = (phi_1_list(k) > 0 & phi_1_list(k) < pi/2) & Phi_list(k) > 60*degree;%60
        
        % add these orientations to inner set
        phi_1_inner = cat(1,phi_1_inner, phi_1_plot(mask));
        Phi_inner = cat(1,Phi_inner, Phi_plot(mask));
        
        % delete them from the boundary set
        phi_1_plot(mask) = [];
        Phi_plot(mask) = [];
    end
    
    % create array for phi2
    phi_2_plot = ones(size(Phi_plot))*v;
    phi_2_inner = ones(size(Phi_inner))*v;
    points_boundary = cat(1, points_boundary, [phi_1_plot, Phi_plot, phi_2_plot(:)]);
    points_inner = cat(1,points_inner, [phi_1_inner, Phi_inner, phi_2_inner]);
end

%Sample phi1,phi2 plane for Phi==90° 
[phi_1, phi_2] = meshgrid(phi1, phi2(1:end));
[nRow, nCol] = size(phi_1);
phi_1_plot = reshape(phi_1, [nRow*nCol, 1]);
phi_2_plot = reshape(phi_2, [nRow*nCol, 1]);
Phi_plot = ones(size(phi_1_plot))*pi/2;
points_boundary = cat(1, points_boundary, [phi_1_plot(:), Phi_plot(:), phi_2_plot(:)]);

ori_boundry = orientation.byEuler(points_boundary, crystalSymmetry("432"), specimenSymmetry("222"));
ori_boundry_projected = ori_boundry.project2FundamentalRegion;
[~, idx_r, ~]  = unique(ori_boundry_projected,'stable', 'tolerance', 0.00001);
points_boundary = points_boundary(idx_r,:);

% % Plotting
% figure
% hold on
% grid on
% xlabel('phi_1')
% ylabel('Phi')
% zlabel('phi_2')
% title(sprintf('Cubic-Orthorhombic FZ - %.1f° resolution',resolution))
% scatter3(points_boundary(:,1)/degree, points_boundary(:,2)/degree, ...
%     points_boundary(:,3)/degree, '.', 'r');
% scatter3(points_inner(:,1)/degree, points_inner(:,2)/degree, ...
%     points_inner(:,3)/degree, '.', 'b');



