#%%
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests


#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.double_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "extended_data"

#%%
barrier_dict_aa = dict(np.load(data_dir / "A2d_barrier_dict_aa.npz",allow_pickle=True))

#%%
num_rates = 0
all_rates = []
noval = []
barrier_dict_aa.pop('all',None)
for k,v in  barrier_dict_aa.items():
    if len(v) < 2:
        noval.append(k)
    num_rates += len(v)
    all_rates.extend(v)
barrier_dict_aa['all'] = all_rates
print(num_rates)

for k in noval:
    barrier_dict_aa.pop(k)

#%%
if barrier_dict_aa.get('PYD',None) is None:
    barrier_dict_aa['PYD'] = []
    barrier_dict_aa['PYD'].extend(barrier_dict_aa['LY2'])
    barrier_dict_aa['PYD'].extend(barrier_dict_aa['LY3'])
    barrier_dict_aa['PYD'].extend(barrier_dict_aa['LYX'])

# %%
p_values_dict = {}
p_values = []
for group_name, group_data in barrier_dict_aa.items():
    if group_name != 'all':  # Skip the 'all' group itself
        t_stat, p_value = stats.ttest_ind(group_data, list(set(barrier_dict_aa['all'])-set(group_data)), equal_var=False,alternative='less')
        p_values_dict[group_name] = p_value
        p_values.append(p_value)

# Apply Benjamini-Hochberg correction for multiple testing
reject, corrected_p_values, _, _ = multipletests(p_values,method='fdr_bh')

# Display results
results = pd.DataFrame({
    'Group': [group for group in barrier_dict_aa if group != 'all'],
    'p-value': p_values,
    'Corrected p-value': corrected_p_values,
    'Reject null': reject
})

print(results)

#%%
palette = sns.color_palette('pastel')
order = ['ALA','LEU','ILE','VAL','MET','TRP','SER','DOP','THR','ASN','GLN','ARG','HIS','LYS','ASP','GLU','CYS','GLY','PRO','HYP','LY2','LY3','LYX']#,'all']


plt.figure(figsize=(width*0.66, width*0.3))
sns.barplot(x='Group', y='Corrected p-value', data=results, order=order, color=palette[7])
plt.axhline(y=0.05, color='r', linestyle='--', label='Significance threshold (0.05)')

for i in [2,5,8,12,16,18]:
    plt.bar(i,1,color='lightgrey',alpha=0.45)

plt.xticks(rotation=90)
plt.xlabel('')
#plt.title('Multiple Hypothesis Testing Results (Corrected p-values)')
plt.ylabel('Corrected p-value')
#plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "multiple-hypothesis-aa.png",dpi=300)

