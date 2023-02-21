function newfield = relax(field,par,dt,geostaticflag)
%RELAX relaxation (source) operator

field = friction(field,par,dt);
field = entrainment(field,par,dt);
field = geomorphic(field,par,dt);
field = knappBagnold(field,par,dt);
field = dissipation(field,par,dt);
field = hemipelagic(field,par,dt);
% if ( geostaticflag == 1 )
%     field = geostatic(field,par);
% end;
newfield = field;