# %%

import matplotlib.pyplot as plt
from myutils.g_values.best_fit import *
import kimmdy_paper_theme


plot_colors = kimmdy_paper_theme.auto_init()
files = ['../DOPA/radical/EPRspectrum.dat',
         '../PYD/radical/EPRspectrum.dat',]


ybottom = 0.08
ytop = 0.95
xleft = 0.06
xright = 0.98
fieldrange = None


tme = TheoMatchExpe(files,
                    experiment_file='../experiments/' +
                                    'Kurth2023_G-band-Achilles.dat')

fig, ax = plt.subplots(2,2)

sp = StandardPlotter(fig=fig, ax=ax.flatten(), set_default=False)

sp.fig.set_size_inches(kimmdy_paper_theme.double_column,
                       1.2 * kimmdy_paper_theme.single_column)
sp.change_general_pars(kimmdy_paper_theme.default_plot_config)

field = (tme.fieldexp + tme.shift)/1000
exp = tme.intensexp
pyd = tme.coeffs[1] * tme.intensities[1]
dopa = tme.coeffs[0] * tme.intensities[0]
with open('severalEPR_SIa.dat', 'w') as f:
    f.write('# field[T]\texp\tpyd\tdopa\n')
    for i in range(len(field)):
        f.write(f'{field[i]:.5f}\t{exp[i]:.6E}\t{pyd[i]:.6E}\t{dopa[i]:.6E}\n')

sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensexp, pstyle='-',
             color_plot='black', data_label='EPR spectrum')
sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensfit, pstyle='-',
             color_plot='gray', data_label='Theoretical\nspectrum')
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[1] * tme.intensities[1], pstyle='-',
             data_label=f'{tme.percentages[1]:.2f}% PYD');
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[0] * tme.intensities[0], pstyle='-',
             data_label=f'{tme.percentages[0]:.2f}% DOPA');

sp.ax[0].set_xlim(((tme.fieldexp + tme.shift)/1000)[0],
                  ((tme.fieldexp + tme.shift)/1000)[-1])
sp.ax[0].set_xlabel('Field [T]')
sp.ax[0].set_ylabel('Intensity [a.u]')
sp.ax[0].legend()

# Second
tme = TheoMatchExpe(files,
                    experiment_file='../experiments/Kurth2023_G-band-Tail.dat')
tme.fit_shifting(tme.files, shifting_width=5)

field = (tme.fieldexp + tme.shift)/1000
exp = tme.intensexp
pyd = tme.coeffs[1] * tme.intensities[1]
dopa = tme.coeffs[0] * tme.intensities[0]
with open('severalEPR_SIb.dat', 'w') as f:
    f.write('# field[T]\texp\tpyd\tdopa\n')
    for i in range(len(field)):
        f.write(f'{field[i]:.5f}\t{exp[i]:.6E}\t{pyd[i]:.6E}\t{dopa[i]:.6E}\n')

sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensexp, pstyle='-',
             color_plot='black', data_label='EPR spectrum', ax=1)
sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensfit, pstyle='-',
             color_plot='gray', data_label='Theoretical\nspectrum', ax=1)
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[1] * tme.intensities[1], pstyle='-',
             data_label=f'{tme.percentages[1]:.2f}% PYD', ax=1);
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[0] * tme.intensities[0], pstyle='-',
             data_label=f'{tme.percentages[0]:.2f}% DOPA', ax=1);

sp.ax[1].set_xlim(((tme.fieldexp + tme.shift)/1000)[0],
                  ((tme.fieldexp + tme.shift)/1000)[-1])
sp.ax[1].set_xlabel('Field [T]')
sp.ax[1].set_ylabel('Intensity [a.u]')
sp.ax[1].legend()

# Third
tme = TheoMatchExpe(files,
                    experiment_file='../experiments/' +
                                    'Kurth2023_G-band-Meniscus.dat')
tme.fit_shifting(tme.files, shifting_width=5)

field = (tme.fieldexp + tme.shift)/1000
exp = tme.intensexp
pyd = tme.coeffs[1] * tme.intensities[1]
dopa = tme.coeffs[0] * tme.intensities[0]
with open('severalEPR_SIc.dat', 'w') as f:
    f.write('# field[T]\texp\tpyd\tdopa\n')
    for i in range(len(field)):
        f.write(f'{field[i]:.5f}\t{exp[i]:.6E}\t{pyd[i]:.6E}\t{dopa[i]:.6E}\n')

sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensexp, pstyle='-',
             color_plot='black', data_label='EPR spectrum', ax=2)
sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensfit, pstyle='-',
             color_plot='gray', data_label='Theoretical\nspectrum', ax=2)
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[1] * tme.intensities[1], pstyle='-',
             data_label=f'{tme.percentages[1]:.2f}% PYD', ax=2);
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[0] * tme.intensities[0], pstyle='-',
             data_label=f'{tme.percentages[0]:.2f}% DOPA', ax=2);

sp.ax[2].set_xlim(((tme.fieldexp + tme.shift)/1000)[0],
                  ((tme.fieldexp + tme.shift)/1000)[-1])
sp.ax[2].set_xlabel('Field [T]')
sp.ax[2].set_ylabel('Intensity [a.u]')
sp.ax[2].legend()

# Fourth
tme = TheoMatchExpe(files,
                    experiment_file='../experiments/Zapp2020.dat')
tme.fit_shifting(tme.files, shifting_width=20)

field = (tme.fieldexp + tme.shift)/1000
exp = tme.intensexp
pyd = tme.coeffs[1] * tme.intensities[1]
dopa = tme.coeffs[0] * tme.intensities[0]
with open('severalEPR_SId.dat', 'w') as f:
    f.write('# field[T]\texp\tpyd\tdopa\n')
    for i in range(len(field)):
        f.write(f'{field[i]:.5f}\t{exp[i]:.6E}\t{pyd[i]:.6E}\t{dopa[i]:.6E}\n')

sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensexp,
             pstyle='-', color_plot='black', data_label='EPR spectrum', ax=3)
sp.plot_data((tme.fieldexp + tme.shift)/1000, tme.intensfit,
             pstyle='-', color_plot='gray', data_label='Theoretical\nspectrum',
             ax=3)
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[1] * tme.intensities[1], pstyle='-',
             data_label=f'{tme.percentages[1]:.2f}% PYD', ax=3);
sp.plot_data((tme.fieldexp + tme.shift)/1000,
             tme.coeffs[0] * tme.intensities[0], pstyle='-',
             data_label=f'{tme.percentages[0]:.2f}% DOPA', ax=3);

sp.ax[3].set_xlim(((tme.fieldexp + tme.shift)/1000)[0],
                  ((tme.fieldexp + tme.shift)/1000)[-1])
sp.ax[3].set_xlabel('Field [T]')
sp.ax[3].set_ylabel('Intensity [a.u]')
sp.ax[3].legend()


# General set-up
sp.spaces[0].set_axis(ax.flatten(), (2, 2), borders=[[xleft, ybottom],
                                                     [xright, ytop]],
                      spaces=(0.1,0.14))
l = 0.02 # left
r = 0.53 # right
u = 0.96 # up
d = 0.46  # down

sp.spaces[0].frame.text(l, u, r'$\bf{a}$', fontsize=10, ha='center',
                        va='center')
sp.spaces[0].frame.text(r, u, r'$\bf{b}$', fontsize=10, ha='center',
                        va='center')
sp.spaces[0].frame.text(l, d, r'$\bf{c}$', fontsize=10, ha='center',
                        va='center')
sp.spaces[0].frame.text(r, d, r'$\bf{d}$', fontsize=10, ha='center',
                        va='center')

# sp.spaces[0].show_frame()
sp.save('several-PYD_DOPA_in_collagenEPR-SI.png')
