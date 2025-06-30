# %%
import ast
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from tqdm.autonotebook import tqdm


#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.single_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "SI"

#%%
df_dict = {}
df_dict["2_6"] = pd.read_csv(data_dir / f"S7abf_rates_5ns_1ps_full.csv",index_col=0)
df_dict["2_6"]['ids'] = df_dict["2_6"]['ids'].apply(ast.literal_eval)


#%%
n_smallest = [1,10,100,1000,10000,50000]
rate_fraction = {k:[] for k in n_smallest}
n_frames = len(df_dict['2_6']['time (fs)'].unique())
for run,df in df_dict.items():
    for _,g in tqdm(df.groupby('ids')):
        if g['translation'].min() > 2:
            continue
        overall_mean = g['rates (1/s)'].sum() #/n_frames
        for n in n_smallest:
            lowest_rows = g.nsmallest(n,'translation')
            rate_fraction[n].append(lowest_rows['rates (1/s)'].sum()/overall_mean)

#%%
plt.figure(figsize=(width, width*0.75))
plt.rcParams.update({'mathtext.default':  'regular' })
scale = 'log'

for i,(n,vals) in enumerate(rate_fraction.items()):
    print(i,np.percentile(vals,q=10))
    plt.boxplot(vals, positions=[i],whis=1.5,labels=[n],showfliers=True,boxprops=dict(linewidth=1.5),medianprops=dict(linewidth=2,color='k'),flierprops=dict(markersize=1,color='k',marker='.'),zorder=4)
    plt.scatter(i,np.percentile(vals,q=10),marker='_',c='darkviolet',zorder=5,s=30)
    plt.scatter(i,np.percentile(vals,q=1),marker='_',c='violet',zorder=5,s=30)
plt.xlabel('Number of Smallest Translation Distances')
plt.ylabel('r$_{predicted}$ / r$_{reference}$ ')
#plt.title('Relative rates calculated from n lowest translations')
if scale == 'log':
    plt.yscale('log')
    plt.ylim((1e-10,2e0))

point_q10 = Line2D([0], [0], label='10%ile', marker='_', markersize=8, 
         markeredgecolor='darkviolet', markerfacecolor='darkviolet', linestyle='')
point_q1 = Line2D([0], [0], label='1%ile', marker='_', markersize=8, 
         markeredgecolor='violet', markerfacecolor='violet', linestyle='')

handles, labels = plt.gca().get_legend_handles_labels()
handles.extend([point_q10,point_q1])
plt.legend(handles=handles)
plt.tight_layout()
plt.savefig(plot_dir / f'translation_rate_nsmallest_{scale}.png',dpi=300)


# %%
