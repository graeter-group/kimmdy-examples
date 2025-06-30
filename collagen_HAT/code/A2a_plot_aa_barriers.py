#%%
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.double_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "extended_data"

#%%
df_aa = pd.read_csv(data_dir / "A2a_aa_barrierdata.csv",index_col=0)

#%%
plt.figure(figsize=(width*0.8,width*0.3))
order = ['ALA','LEU','ILE','VAL','MET','TRP','SER','DOP','THR','ASN','GLN','ARG','HIS','LYS','ASP','GLU','CYS','GLY','PRO','HYP','LY2','LY3','LYX']#,'all']
palette = sns.color_palette('pastel')


sns.violinplot(data=df_aa, x='AA', y='Barrier', order = order,hue='Color',legend=False,common_norm=False,width=0.8,density_norm='area',palette=palette,saturation=1,inner=None)
sns.stripplot(data=df_aa, x='AA', y='Barrier', order = order, color='k', dodge=False, jitter=False,marker='o', alpha=0.3, legend=False,size=2)


plt.xticks(rotation=90)
plt.xlabel(None)
plt.ylabel('Barrier [kcal/mol]')
plt.savefig(plot_dir / "violin-barrier-aa-thesis.png",dpi=300),
# %%
