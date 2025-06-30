# %%
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.single_column


#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "SI"

#%%  S7c
n_elements = 5
suffix = "all"

dfs = []
for csv_file in (data_dir / "S7cd").glob(f"*{suffix}.csv"):
    print(csv_file)
    try:
        df_in = pd.read_csv(csv_file,index_col=0)
        sim = f"{csv_file.name.split(sep='_')[2]}_{csv_file.name.split(sep='_')[3]}"
        df_in['simulation'] = sim
        dfs.append(df_in)
    except:
        print(f"Didn't process csv {csv_file}")
        continue

df = pd.concat(dfs,ignore_index=True)
df = df.sort_values(by='simulation', key=lambda x: [tuple(int(i) for i in val.split('_')) for val in x])
df = df[~df['simulation'].str.startswith('24_8')]     # some trj issues with breakpairs 24
df = df[~df['simulation'].str.startswith('24_10')]     # some trj issues with breakpairs 24
print(len(dfs),'\n',df)


# Calculate mean and standard error for the first n_elements columns
mean = df.iloc[:, :n_elements].mean()
stderr = df.iloc[:, :n_elements].sem()

sum_values = df.iloc[:, n_elements:].sum(axis=1,numeric_only=True,skipna=True)

# Calculate mean and standard error for the sum
rest_mean = sum_values.mean()
rest_stderr = sum_values.sem()

# Plot
plt.figure(figsize=(width,width*0.75))
plt.bar(mean.index, mean, yerr=stderr, capsize=5,color='skyblue')
plt.bar(n_elements,rest_mean,yerr=rest_stderr,capsize=5,color='skyblue')

for i in range(n_elements):
    x_scatter = np.random.normal(loc=i, scale=0.05, size=len(df.iloc[:, i]))
    plt.scatter(x_scatter, df.iloc[:, i], color='black', alpha=1,s=1)
x_scatter = np.random.normal(loc=n_elements, scale=0.05, size=len(sum_values))
plt.scatter(x_scatter, sum_values, color='black', alpha=1)

plt.xticks(range(n_elements+1),list(range(1,n_elements+1))+[f'>{n_elements}'])
plt.xlabel('Reaction rank by rate')
plt.ylabel('r$_{i}$ / r$_{tot}$ (mean ± SE)')
#plt.title(f'Relative Rates from {csv_type}, 7 simulations')
plt.tight_layout()
plt.savefig(plot_dir / f"relative_rates_{suffix}_top{n_elements}.png",dpi=300)

#%%  S7d
n_elements = 5
suffix = "top100translation"

dfs = []
for csv_file in (data_dir / "S7cd").glob(f"*{suffix}.csv"):
    print(csv_file)
    try:
        df_in = pd.read_csv(csv_file,index_col=0)
        sim = f"{csv_file.name.split(sep='_')[2]}_{csv_file.name.split(sep='_')[3]}"
        df_in['simulation'] = sim
        dfs.append(df_in)
    except:
        print(f"Didn't process csv {csv_file}")
        continue


df = pd.concat(dfs,ignore_index=True)
df = df.sort_values(by='simulation', key=lambda x: [tuple(int(i) for i in val.split('_')) for val in x])
df = df[~df['simulation'].str.startswith('24_8')]     # some trj issues with breakpairs 24
df = df[~df['simulation'].str.startswith('24_10')]     # some trj issues with breakpairs 24
print(len(dfs),'\n',df)


# Calculate mean and standard error for the first n_elements columns
mean = df.iloc[:, :n_elements].mean()
stderr = df.iloc[:, :n_elements].sem()

sum_values = df.iloc[:, n_elements:].sum(axis=1,numeric_only=True,skipna=True)

# Calculate mean and standard error for the sum
rest_mean = sum_values.mean()
rest_stderr = sum_values.sem()

# Plot
plt.figure(figsize=(width,width*0.75))
plt.bar(mean.index, mean, yerr=stderr, capsize=5,color='skyblue')
plt.bar(n_elements,rest_mean,yerr=rest_stderr,capsize=5,color='skyblue')

for i in range(n_elements):
    x_scatter = np.random.normal(loc=i, scale=0.05, size=len(df.iloc[:, i]))
    plt.scatter(x_scatter, df.iloc[:, i], color='black', alpha=1,s=1)
x_scatter = np.random.normal(loc=n_elements, scale=0.05, size=len(sum_values))
plt.scatter(x_scatter, sum_values, color='black', alpha=1)

plt.xticks(range(n_elements+1),list(range(1,n_elements+1))+[f'>{n_elements}'])
plt.xlabel('Reaction rank by rate')
plt.ylabel('r$_{i}$ / r$_{tot}$ (mean ± SE)')
#plt.title(f'Relative Rates from {csv_type}, 7 simulations')
plt.tight_layout()
plt.savefig(plot_dir / f"relative_rates_{suffix}_top100translation_top{n_elements}.png",dpi=300)
