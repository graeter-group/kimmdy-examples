# %%
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.single_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "SI"


#%%
data = np.load(data_dir / 'S6ab_mean_barriers.npz', allow_pickle=True)
mean_barrier = data['arr_0'].item()
#%%
for k,v in mean_barrier.items():
    print(k,len(v))
    print(k,np.min(v))
    print(k,np.median(v))
    print(k,np.quantile(v,0.1))
    print(k,np.quantile(v,0.05))
    print('\n')

# %%
plt.figure(figsize=(width,width*0.75))
ax = sns.violinplot(mean_barrier,bw_adjust=0.5,inner=None,legend=False)
sns.stripplot(mean_barrier, jitter=0.1, color='k', alpha=0.15, dodge=True, ax=ax,legend=False,size=2)
plt.xlabel('Number of Conformations')
plt.xticks([0,1,2,3,4,5],[r'10$^2$',r'10$^3$',r'5x10$^3$',r'10$^4$',r'5x10$^4$',r'10$^5$'])
#plt.yticks([1e-70,1e-50,1e-30,1e-10])
plt.ylabel('Barrier of Mean Rate [kcal/mol]')
plt.tight_layout()
plt.savefig(plot_dir / f'n_conformations_barriers_whole.png',dpi=300)

# %%
plt.figure(figsize=(width,width*0.75))
ax = sns.violinplot(mean_barrier,bw_adjust=0.5,inner=None,legend=False)
sns.stripplot(mean_barrier, jitter=0.1, color='k', alpha=0.15, dodge=True, ax=ax,legend=False,size=2)
plt.ylim(20,60)

plt.xticks([0,1,2,3,4,5],[r'10$^2$',r'10$^3$',r'5x10$^3$',r'10$^4$',r'5x10$^4$',r'10$^5$'])
plt.yticks([20,40,60])

plt.xlabel('Number of Conformations')
plt.ylabel('Barrier of Mean Rate [kcal/mol]')
plt.tight_layout()

plt.savefig(plot_dir / f'n_conformations_barriers_cutout.png',dpi=300)
# %%
