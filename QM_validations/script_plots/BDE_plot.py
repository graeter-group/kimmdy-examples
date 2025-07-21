# Figure 3.f
import matplotlib.pyplot as plt
import pandas as pd
from myutils.plotters import StandardPlotter
import numpy as np
import kimmdy_paper_theme
from myutils.miscellaneous import output_terminal


# ==== Our calculation of the iso BDE =========================================
def enthalpy(file):
    """
    Extracts the Enthalpy from an ORCA .out file
    """
    Eh2Kcalm = 627.509
    return float(output_terminal(f"grep \"Total Enthalpy\" {file}" +
                                 "| awk '{print $4}'", print_output=False)) \
           * Eh2Kcalm


# Phenol information
phenol_reactant = enthalpy("../phenol/reactant/phenol_freq.out")
phenol_radical = enthalpy("../phenol/radical/phenol_freq.out")
bde_experiment = 86.7113
constant = phenol_reactant - phenol_radical + bde_experiment

# Our calculated BDE for DOPA in kcal/mol
H_DOPA_radic = enthalpy("../DOPA/radical/DOPA_freq.out")
H_DOPA_react = enthalpy(("../DOPA/reactant/DOPA_freq.out"))
bde_dopa = H_DOPA_radic - H_DOPA_react + constant
print("BDE of DOPA is: ", bde_dopa)

# Our calculated BDE for PYD in kcal/mol
H_PYD_radic = enthalpy("../PYD/radical/PYD_freq.out")
H_PYD_react = enthalpy(("../PYD/reactant/PYD_freq.out"))
bde_pyd = H_PYD_radic - H_PYD_react + constant
print("BDE of PYD is: ", bde_pyd)

# ==== BDEs from dataset ======================================================
# BDEs obtained from: Treyde, W., Riedmiller, K. & Greater, F. Bond
# dissociation energies of X–H bonds in proteins. RSC Advances 12,
# 34557–34564 (2022).
# URL https://xlink.rsc.org/?DOI=D2RA04002F.
bdes = np.loadtxt('../BDEs.dat')

# ==== plot ===================================================================
# Figure set up
ybottom = 0.16
ytop = 0.92
xleft = 0.11
xright = 0.98
plot_colors = kimmdy_paper_theme.auto_init()
sp = StandardPlotter(set_default=False)
width = kimmdy_paper_theme.single_column
sp.fig.set_size_inches(width, 0.63 * width)
sp.change_general_pars(kimmdy_paper_theme.default_plot_config)
sp.ax[0].set_xlabel('BDE [kcal/mol]')
sp.ax[0].set_ylabel('Count')
# locate borders
sp.spaces[0].set_axis(borders=[[xleft, ybottom], [xright, ytop]])

# Add data to the plot
n, bins, patches = sp.ax[0].hist(bdes[bdes != 0], color=(0.8, 0.8, 0.8),
                                 bins=20, range=(59.7515, 131.4533))
new_ax = sp.add_space(borders=[[xleft, 0], [xright, 1]])
new_ax.show_frame(layer='front', majordelta=1, minordelta=1)

# text labels
text_distance = 11 * 0.239006
new_ax.frame.text((bde_pyd + bde_dopa)/2 + text_distance/2, ytop + 0.02, 'PYD',
                  color='C0', ha='left', fontsize=7)
new_ax.frame.text((bde_pyd + bde_dopa)/2 - text_distance/2, ytop + 0.02, 'DOPA',
                  color='C1', ha='right', fontsize=7)
# vertical lines
sp.plot_data([bde_dopa, bde_dopa], [ybottom, ytop], color_plot='C1',
             ax=new_ax.frame, pstyle='-')
sp.plot_data([bde_pyd, bde_pyd], [ybottom, ytop], color_plot='C0',
             ax=new_ax.frame, pstyle='-')

sp.axis_setter(new_ax.frame, xlim=list(sp.ax[0].get_xlim()),
               ylim=[0,1], xticks=sp.ax[0].get_xticks())
new_ax.hide_frame()

# overlap a new frame to hide border of terminal lines
ol = sp.add_axes()
ol.patch.set_alpha(0)
ol.set_xticks([])
ol.set_yticks([])
sp.spaces[0].set_axis(borders=[[xleft, ybottom], [xright, ytop]], axes=[ol])

# save the figure.
# sp.save('PYD_in_BDEs.png')
