#%%
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.single_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "main"

#%%
barrier_dict = dict(np.load(data_dir / "2d_barrier_dict.npz",allow_pickle=True))
#barrier_dict = {k:v.flatten()[0] for k,v in barrier_dict.items()}

# %%

# Perform Welch's t-test
t_stat, p_value = stats.ttest_ind(barrier_dict['DOPA_R_educt-O'],barrier_dict['other'], equal_var=False, alternative='greater')

print("T-statistic:", t_stat)
print("P-value:", p_value)
# %%
t_stat, p_value = stats.ttest_ind(barrier_dict['DOPA_R_product-O'],barrier_dict['other'], equal_var=False, alternative='less')

print("T-statistic:", t_stat)
print("P-value:", p_value)

# %%
barriers_rows = []
for k,v in barrier_dict.items():
    for val in v:
        barriers_rows.append({'HAT type':k,'barrier [kcal/mol]':val})

df = pd.DataFrame(barriers_rows)
# %%
palette = sns.color_palette('pastel')
palette = [palette[7], palette[1]]
df['Color'] = df['HAT type'].apply(lambda x: 0 if x == 'other' else 1)


#%%
plt.figure(figsize=(width, 0.75 * width))
sns.violinplot(x='HAT type', y='barrier [kcal/mol]', data=df, hue='Color',palette=palette,
               order=['DOPA_R_product-O','DOPA_R_educt','other'],inner='box', legend=False)

# Mark significant difference with a star
# statistical annotation
x1, x2 = 1, 2   
y, h, col = 52, 2, 'k'

plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=0.8,c=col)
plt.text((x1+x2)*.5, y+h, "ns", ha='center', va='bottom', color=col,fontsize=7)

# statistical annotation
x1, x2 = 0, 2  
y, h, col = 45, 2, 'k'

plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=0.8, c=col)
plt.text((x1+x2)*.5, y+h, "***", ha='center', va='bottom', color=col,fontsize=7)


plt.xticks([0,1,2],['H-donor\n DOPA-O', 'H-acceptor\n DOPA-O', 'non\nDOPA'],rotation=0)
plt.xlabel('')
plt.ylabel('Barriers [kcal/mol]')

plt.ylim(0,59)

# Show the plot
plt.tight_layout()
plt.savefig(plot_dir / "DOPA_paper.png",dpi=300)

# %%
for k,v in barrier_dict.items():
    print(k,len(v))
    print(np.median(v))
# %%
