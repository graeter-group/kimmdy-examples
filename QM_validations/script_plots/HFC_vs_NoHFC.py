import matplotlib.pyplot as plt
from myutils.g_values.best_fit import TheoMatchExpe
from myutils.plotters import StandardPlotter
import kimmdy_paper_theme

plot_colors = kimmdy_paper_theme.auto_init()

ybottom = 0.16
ytop = 0.92
xleft = 0.06
xright = 0.98

# With hyperfine interactions
fieldrange = None
files = ['../DOPA/radical/EPRspectrum.dat',
         '../PYD/radical/EPRspectrum.dat']

tme = TheoMatchExpe(files,
                    experiment_file='../experiments/' +
                                    'Kurth2023_G-band-Achilles.dat',
                    fieldrange=fieldrange)

fig, ax = plt.subplots(1,2)
sp = StandardPlotter(fig=fig, ax=ax, set_default=False)
sp.fig.set_size_inches(kimmdy_paper_theme.double_column,
                       0.6 * kimmdy_paper_theme.single_column)
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
sp.ax[0].set_xlabel('Field [T]')
sp.ax[0].set_ylabel('Intensity [a.u]')
sp.ax[0].set_title('With hyperfine corrections')
sp.ax[0].legend()

# Second
# Without hyperfine interactions
files = ['../DOPA/radical/EPRspectrum.dat',
         '../PYD/radical/EPRspectrum_NoHFC.dat']
tme = TheoMatchExpe(files,
                    experiment_file='../experiments/' +
                                    'Kurth2023_G-band-Achilles.dat',
                    fieldrange=fieldrange)

sp.plot_data(tme.fieldexp/1000, tme.intensexp, pstyle='-', color_plot='black',
             data_label='EPR spectrum', ax=1)
sp.plot_data(tme.fieldexp/1000, tme.intensfit, pstyle='-', color_plot='gray',
             data_label='Theoretical\nspectrum', ax=1)
sp.plot_data(tme.fieldexp/1000, tme.coeffs[1] * tme.intensities[1], pstyle='-',
             data_label='PYD', ax=1);\
sp.plot_data(tme.fieldexp/1000, tme.coeffs[0] * tme.intensities[0], pstyle='-',
             data_label=r'DOPA', ax=1);

sp.ax[1].set_xlim(((tme.fieldexp + tme.shift)/1000)[0],
                  ((tme.fieldexp + tme.shift)/1000)[-1])

sp.ax[1].set_xlabel('Field [T]')
sp.ax[1].set_ylabel('Intensity [a.u]')
sp.ax[1].set_title('Without hyperfine corrections')
sp.ax[1].legend()


sp.spaces[0].set_axis(ax, (1, 2), borders=[[xleft, ybottom], [xright, ytop]],
                      spaces=(0.07,0))

# sp.save('PYD_in_collagenEPR-SI.png')
