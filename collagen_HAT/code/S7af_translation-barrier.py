#%%
import ast
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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

# %% S7a
plt.figure(figsize=(width,width*0.75))
sns.scatterplot(data=df_dict['2_6'],x='translation',y='barriers (kcal/mol)',s=1,c='dimgrey',alpha=0.1,edgecolor=None)
plt.xlim(1,3.1)
plt.xticks()

plt.xticks([1,2,3])
plt.xlabel('Translation [Å]')
plt.ylabel('Barriers [kcal/mol]')
plt.tight_layout()
plt.savefig(plot_dir / f"reaction-over-translation_full.png",dpi=300)

#%% S7f plot barrier over time with nsmallest
df_test = df_dict['2_6']
# Get the unique ids
unique_ids = [('278447','313306')]

# Iterate over chunks of 20 unique ids
for current_id in unique_ids:
    df_id = df_test[df_test['ids'] == current_id]
    df_id = df_id.sort_values('time (fs)')


    plt.figure(figsize=(width*1.33, width*0.75))
    plt.scatter(df_id['time (fs)']/1e6, df_id['barriers (kcal/mol)'], alpha=1,s=1,c='darkgrey')

    df_nsmallest = df_id.nsmallest(100,columns='translation')
    plt.scatter(df_nsmallest['time (fs)']/1e6, df_nsmallest['barriers (kcal/mol)'],alpha=1,s=2,c='r',zorder=5)

    # Adding labels and title
    plt.xlabel('Time [ns]')
    plt.ylabel('Barriers [kcal/mol]')

    plt.tight_layout()
    plt.savefig(plot_dir / f"reaction-over-time_nsmallest_{'-'.join(current_id)}.png",dpi=300)
# %%
