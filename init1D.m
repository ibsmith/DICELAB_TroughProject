function field = init3Reaches(n,par)
%INITFIELD initialise flow field
%
% n = number of cells per unit block length

L1 = 15000; % length of reach 6000
S1 = 0.003; % slope of reach 1 (originaly 0.013)
p1 = 0; % amplitude of initial bed perturbation for reach 1
L2 = 15000; % 6000
S2 = 0.003; % 0.006
p2 = 0;
L3 = 5000;
S3 = 0;
p3 = 0;

field.S1 = S1;
field.S2 = S2;
field.S3 = S3;
field.L1 = L1;
field.L2 = L2;
field.L3 = L3;
field.pert1 = p1;
field.pert2 = p2;
field.pert3 = p3;

% initialise flow domain:
x0 = -L1;
Lx = L1+L2+L3; % 1 m
y0 = 0;
Ly = 0.5; % 1 m
dx = Lx/n;
dy=dx;
x = (x0-0.5*dx):dx:(x0+Lx+0.5*dx);
y = 1; %(y0-0.5*dy):dy:(y0+Ly+0.5*dy);
field.x = ones(length(y),1) * x;
field.y = y' * ones(1,length(x));

isX1 = find((field.x>-field.L1)&(field.x<0));
isX2 = find((field.x>0)&(field.x<field.L2));
isX3 = find((field.x>field.L2)&(field.x<(field.L2+field.L3)));

% top of turbid layer:
field.z_m = ones( size(field.x) )*-1000;%.001;
% field.z_m(field.x<0) = 0.75;

% turbid concentration
field.c_m = ones( size(field.x) )*0;%.0001;
% field.c_m(field.x<0) = 0.2;

% turbulent kinetic energy
field.k_m = ones( size(field.x) )*0;%.0001;

% rigid channel bottom under sediment bed:
field.z_r = ones( size(field.x) )*-2000; % default
% known points for interpolation
% xx = [-1e10   0 1e10];
% zz = [1e10*S1 0 -1e10*S1];
% field.z_r = interp1(xx,zz,field.x);
field.z_r(end-2:end) = -1000;

% sediment bed level:
field.z_b = ones( size(field.x) )*-1000; % default
% known points for interpolation
xx = [-L1   0 L2     L2+L3];
zz = [L1*S1 0 -L2*S2 -L2*S2-L3*S3];
field.z_b = interp1(xx,zz,field.x,'linear','extrap');
field.z_b(end-2:end) = -1000;
% rigid rim around domain (downstream only):
field.z_r([end]) = 1000;

%initial bed perturbations
field.z_b(isX1) = field.z_b(isX1) + ( rand(size(field.z_b(isX1)))*p1-p1/2 );
field.z_b(isX2) = field.z_b(isX2) + ( rand(size(field.z_b(isX2)))*p2-p2/2 );
field.z_b(isX3) = field.z_b(isX3) + ( rand(size(field.z_b(isX3)))*p3-p3/2 );

% upstream inflow section
field.H_up = 60;
field.C_up = 0.0015;
field.U_up = 1;
% field.Ri_up = 0.8;
% field.U_up = (par.R*par.g*field.C_up*field.H_up/field.Ri_up)^0.5;
field.Q_up = field.H_up*field.U_up;
field.K_up = par.CfStar/par.alpha*field.U_up^2; % assume turbulence is fully developed at inflow


% z-ordering condition:
field.z_b = max( field.z_b , field.z_r );
field.z_m = max( field.z_m , field.z_b );

% velocities:
field.u = zeros( size(field.x) );
field.v = zeros( size(field.x) );

% time:
% -----
field.t = 0;
