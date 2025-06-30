#%%
from pathlib import Path
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.single_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "main"

#%%
df = pd.read_csv(data_dir / "2c_min_distances3.csv", index_col = 0)
df['Inner Key'] = df['Inner Key'] + 1
#%%
# Create the swarmplot
plt.figure(figsize=(width*0.9, width*0.75))
#sns.violinplot(x='Inner Key', y='Value', data=df,legend=False,common_norm=False,width=0.8,density_norm='area',saturation=1,inner=None)
sns.stripplot(x='Inner Key', y='Value', color='k', data=df,legend=False,alpha=0.5,size=2)

plt.xticks([0,4,9,14,19])
plt.xlim((-0.5,20.5))
plt.yticks((0,5,10,15))
plt.ylim((-0.5,17))

plt.xlabel('Reaction #')
#plt.ylabel("Radical distance to initial radical ")
plt.ylabel('Distance [Å]')
plt.tight_layout()
plt.savefig(plot_dir / "diffusion_dist.png", dpi=300)

#%%
palette = sns.color_palette('pastel')

plt.figure(figsize=(width*0.1, width*0.75))
sns.violinplot(x='Inner Key', y='Value', data=df,order=[20],legend=False,common_norm=False,width=0.8,
               density_norm='area',saturation=1,inner=None, split=True,cut=0,bw_adjust=0.3,color=palette[7])
plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                labelbottom=False, labelleft=False)  # Remove all ticks and labels
plt.ylim((-0.5,17))
plt.xlabel('')  # Remove x-axis label
plt.ylabel('')  # Remove y-axis label
plt.tight_layout()
plt.savefig(plot_dir / "diffusion_dist_violin.png", dpi=300)
