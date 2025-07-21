clear, clf, clc
data = readmatrix('../../experiment/field_intensity.dat');
field = data(:,1)
% ==== Experiment
Exp.mwFreq = 179.818;
Exp.Range = [min(field) max(field)];
Exp.nPoints = 401;
Exp.Harmonic = 0;

% ==== Theory
Sys = orca2easyspin('./PYD_epr.out');
Sys.lwpp = 0.5 ;

[ field, spec ] = pepper(Sys, Exp);
data = [field(:), spec(:) ];
writematrix(data, './EPRspectrum.dat', 'Delimiter', 'tab');
