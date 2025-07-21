import matplotlib.pyplot as plt
from myutils.plotters import StandardPlotter
from myutils.g_values.best_fit import TheoMatchExpe
import kimmdy_paper_theme
from sklearn.metrics import r2_score


plot_colors = kimmdy_paper_theme.auto_init()

ybottom = 0.16
ytop = 0.92
xleft = 0.11
xright = 0.98

fieldrange = None
files = ['../DOPA/radical/EPRspectrum.dat']
tme = TheoMatchExpe(files,
                    experiment_file='../experiments/' +
                                    'Kurth2023_G-band-Achilles.dat',
                    fieldrange=fieldrange,
                    shifting_width=0)

exper = tme.intensexp
fit = tme.intensfit
r2 = r2_score(exper, fit/max(fit))
print("r^2 Only dopa: ", r2)

files = ['../DOPA/radical/EPRspectrum.dat',
         '../PYD/radical/EPRspectrum.dat']

tme = TheoMatchExpe(files,
                    experiment_file='../experiments/' +
                                    'Kurth2023_G-band-Achilles.dat',
                    fieldrange=fieldrange,
                    shifting_width=10)

exper = tme.intensexp
fit = tme.intensfit
r2 = r2_score(exper, fit)
print("r^2 dopa and PYD: ", r2)

sp = StandardPlotter(set_default=False)

width = kimmdy_paper_theme.single_column
sp.fig.set_size_inches(width, 0.63 * width)
sp.change_general_pars(kimmdy_paper_theme.default_plot_config)

sp.plot_data(tme.fieldexp/1000, tme.intensexp, pstyle='-', color_plot='black',
             data_label='EPR spectrum')
sp.plot_data(tme.fieldexp/1000, tme.intensfit, pstyle='-', color_plot='gray',
             data_label='Theoretical\nspectrum')

sp.plot_data(tme.fieldexp/1000, tme.coeffs[1] * tme.intensities[1], pstyle='-',
             data_label=r'PYD');
sp.plot_data(tme.fieldexp/1000, tme.coeffs[0] * tme.intensities[0], pstyle='-',
             data_label=r'DOPA');

sp.ax[0].set_xlim(((tme.fieldexp + tme.shift)/1000)[0],
                  ((tme.fieldexp + tme.shift)/1000)[-1])
sp.spaces[0].set_axis(borders=[[xleft, ybottom], [xright, ytop]])
sp.ax[0].set_xlabel('Field [T]')
sp.ax[0].set_ylabel('Intensity [a.u]')
sp.ax[0].legend()

#sp.save('PYD_in_collagenEPR.png')
