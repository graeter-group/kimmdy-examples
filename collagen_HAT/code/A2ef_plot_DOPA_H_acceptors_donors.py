#%%
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.double_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "extended_data"

# %%
rates_by_H_acceptor = dict(np.load(data_dir /  "A2e_rates_by_H_acceptor.npz",allow_pickle=True))


# %%
num_reactions = {}
sum_reactions = 0
for k,v in rates_by_H_acceptor.items():
    print(k,len(v))
    sum_reactions += len(v)
    num_reactions[k] = len(v)
print(f"{sum_reactions} reactions!")

#%%
df_rows = []
for k,v in num_reactions.items():
    if k in ['LY2_CA','LY2_CB']:
        c = 0
    elif k[:3] in ['LY2','LY3','LYX']:
        c = 1
    else:
        if k == 'DO2_OH2':
            k = 'DOP_OH2'
        c = 2
    k = k.replace('_','\n')
    df_rows.append({'atom':k,'n_samples':v,'color':c})

df_1 = pd.DataFrame(df_rows)

# %%
palette = sns.color_palette('pastel')
palette = [palette[5], palette[6],palette[7]]

#%%
# Create a bar plot using Seaborn
plt.figure(figsize=(0.47*width,0.3*width))
sns.barplot(x='atom',y='n_samples',data=df_1,hue='color',palette=palette,legend=False,
            order = ['LY2\nCA','LY2\nCB','ARG\nNH1','ARG\nNH2','DOP\nOH2','GLY\nN','LYX\nO11'],
            )
plt.xlabel('')
plt.ylabel('Reaction count')


plt.yticks([0,5,10,15])
plt.tight_layout()
plt.savefig(plot_dir / "DOPA_H_acceptor_occurence.png",dpi=300)
# %%
# %%
rates_by_H_donor = dict(np.load(data_dir / "A2f_rates_by_H_donor.npz",allow_pickle=True))


# %%
num_reactions = {}
sum_reactions = 0
for k,v in rates_by_H_donor.items():
    print(k,len(v))
    sum_reactions += len(v)
    num_reactions[k] = len(v)
print(f"{sum_reactions} reactions!")

#%%
df_rows = []
for k,v in num_reactions.items():
    if k in ['LY2_CA','LY2_CB']:
        #c = 0 #doesnt exist
        pass
    elif k[:3] in ['LY2','LY3','LYX']:
        c = 1
    else:
        if k == 'DO2_OH2':
            k = 'DOP_OH2'
        c = 2
    k = k.replace('_','\n')
    df_rows.append({'atom':k,'n_samples':v,'color':c})

df_2 = pd.DataFrame(df_rows)

# %%
palette = sns.color_palette('pastel')
palette = [ palette[6],palette[7]]

#%%
# Create a bar plot using Seaborn
plt.figure(figsize=(0.53*width,0.3*width))
sns.barplot(x='atom',y='n_samples',data=df_2,hue='color',palette=palette,legend=False,
            order = ['ARG\nNH1','ARG\nNH2','HYP\nOD1','ASP\nN','GLN\nNE2','ARG\nNE','LYS\nNZ','LYX\nO11'],
            )
plt.xlabel('')
plt.ylabel('Reaction count')


plt.yticks([0,5,10,15])
plt.tight_layout()
plt.savefig(plot_dir / "DOPA_H_donor_occurence.png",dpi=300)
# %%
