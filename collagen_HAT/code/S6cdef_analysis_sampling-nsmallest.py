# %%
import csv
import ast
import colorsys
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import pickle
from scipy import stats
import shutil

from tqdm.autonotebook import tqdm
from kimmdy.recipe import Break, RecipeCollection, Recipe
import pandas as pd

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.double_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "SI"

#%% functions
def calculate_activation_energy(rate, A=0.288e12, T=300):
    """
    Calculate the activation energy from the rate using the Arrhenius equation.
    
    Parameters:
        rate (float): The rate constant k.
        A (float): The pre-exponential factor. [1/s]
        T (float): The temperature in Kelvin.

    Returns:
        float: The activation energy in joules per mole.
    """
    R = 1.9872159e-3  # Gas constant in kcal/(mol*K)
    Ea = -R * T * np.log(rate / A)
    return Ea


#%%
root = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/HAT_benchmark/")
runs = ['2_6','2_8','2_10']
sims = ['500ps','5ns','50ns']
basenames = ["500ps_10fs","5ns_1ps","50ns_10ps"]


#%% load data
df_dict = {'500ps':{},'5ns':{},'50ns':{}}
experiment = "repeats"

for sim, basename in zip(sims,basenames):
    for run in runs[:]:
        print(sim,run)
        try:
            df_dict[sim][run] = pd.read_csv(data_dir / "S6cdef" / f"rates_{basename}_{run}_full.csv",index_col=0)
            df_dict[sim][run]['ids'] = df_dict[sim][run]['ids'].apply(ast.literal_eval)
        except FileNotFoundError:
            print(f"No file found for {sim},{run}")
            continue
print(df_dict[sim].keys())

#%% need to merge data because 50ns run started after 5ns run
for run in ['2_6','2_8','2_10']:
    print(run)
    df_5ns_filtered = df_dict['5ns'][run][df_dict['5ns'][run]['time (fs)'] % 1000 == 0]
    print(len(df_5ns_filtered))
    df_50ns_filtered = df_dict['50ns'][run][df_dict['50ns'][run]['time (fs)'] < 4.5e7]
    df_50ns_filtered['time (fs)'] = df_50ns_filtered['time (fs)'] + 5e6
    print(len(df_50ns_filtered))
    df_dict['50ns'][run] = pd.concat([df_5ns_filtered,df_50ns_filtered],ignore_index=True)

#%% get nsmallest for 5ns and 50ns
n_frames = 50000
#data_transform = 'raw'
data_transform = 'below2A'
#data_transform = 'same_confs'


rate_dicts = []

#500ps data has nsmallest 100 already
print('500ps')
for run,df in df_dict['500ps'].items():
    for idx in df['ids'].unique():
        df_nsmallest = df[df['ids'] == idx].nsmallest(100, 'translation')
        mean_barrier = calculate_activation_energy(np.sum(df[df['ids']==idx]['rates (1/s)'])/n_frames)
        if data_transform in ['below2A','same_confs']:
            if df_nsmallest.iloc[0]['translation'] > 2:
                continue
        rate_dicts.append({'sim':'500ps','run':run, 'ids': idx, 'barrier (kcal/mol)':mean_barrier, })

# calculate nsmallest for 5ns, 50ns
for sim in ['5ns','50ns']:
    print(sim)
    for run,df in df_dict[sim].items():
        for idx in df['ids'].unique():
            if data_transform == 'same_confs':
                if sim == '5ns':
                    sub_df = df[(df['time (fs)'] % 1000) == 0]
                elif sim == '50ns':
                    sub_df = df[df['time (fs)'] < 5e6] 
                df_nsmallest = sub_df[sub_df['ids'] == idx].nsmallest(100, 'translation')
                if len(df_nsmallest) ==0:
                    continue
            else:
                df_nsmallest = df[df['ids'] == idx].nsmallest(100, 'translation')
            mean_barrier = calculate_activation_energy(np.sum(df_nsmallest[df_nsmallest['ids']==idx]['rates (1/s)'])/n_frames)
            if data_transform in ['below2A','same_confs']:
                if df_nsmallest.iloc[0]['translation'] > 2:
                    continue
            rate_dicts.append({'sim':sim,'run':run, 'ids': idx, 'barrier (kcal/mol)':mean_barrier})

# %%
rate_df = pd.DataFrame(rate_dicts)

#%%
min_barriers = {}
for sim in sims:
    min_barriers[sim] = rate_df[rate_df['sim'] == sim]['barrier (kcal/mol)'].min()

# %%
# Plot using seaborn's violinplot
plt.figure(figsize=(10, 6))
ax = sns.violinplot(x='sim', y='barrier (kcal/mol)', hue='sim', data=rate_df,inner=None,legend=False,palette='deep')
sns.stripplot(x='sim', y='barrier (kcal/mol)', data=rate_df, jitter=0.05, color='k', alpha=0.15, dodge=True, ax=ax,legend=False)
plt.xlabel('Simulation time')
plt.ylabel('barrier of mean rate [kcal/mol]')

plt.ylim((15,140))

plt.text(-0.45,123,f"# reactions:")
plt.text(0.05,123,f"{len(rate_df[rate_df['sim'] == '500ps'])}")
plt.text(1.05,123,f"{len(rate_df[rate_df['sim'] == '5ns'])}")
plt.text(2.05,123,f"{len(rate_df[rate_df['sim'] == '50ns'])}")

plt.text(-0.45,128,f"min barrier:")
plt.text(0.05,128,f"{min_barriers['500ps']:.1f}")
plt.text(1.05,128,f"{min_barriers['5ns']:.1f}")
plt.text(2.05,128,f"{min_barriers['50ns']:.1f}")

plt.savefig(plot_dir / f"sampling-paper-violin-{data_transform}.png",dpi=300)

# %% set differences
rate_df['run_ids'] = rate_df.apply(lambda row: (row['ids'][0], row['ids'][1], row['run']), axis=1)

# %%
for A,B,C in [['500ps','5ns','50ns'],['5ns','50ns','500ps'],['500ps','50ns','5ns']]:
    print(A,B)
    colors = sns.color_palette('deep')
    c_vals = [colors[sims.index(A)],colors[sims.index(B)]]

    set_A = set(rate_df[rate_df['sim'] == A]['run_ids'].unique())
    set_B = set(rate_df[rate_df['sim'] == B]['run_ids'].unique())

    A_minus_B = set_A - set_B
    intersectAB = set_A & set_B
    B_minus_A = set_B - set_A

    # Add the new column 'status' based on the conditions
    curr_df = rate_df
    curr_df['status'] = curr_df['run_ids'].apply(lambda x: 'diffA' if x in A_minus_B 
              else ('diffB' if x in B_minus_A 
                    else ('intersectAB' if x in intersectAB else 'none')))
    
    curr_df = curr_df[curr_df['sim'] != C]

    #calculate statistics
    min_barriers = {}
    min_barriers['diffA'] = curr_df[curr_df['status'] == 'diffA']['barrier (kcal/mol)'].min()
    min_barriers['diffB'] = curr_df[curr_df['status'] == 'diffB']['barrier (kcal/mol)'].min()
    min_barriers['AintersectAB'] = curr_df[(curr_df['status'] == 'intersectAB') & (curr_df['sim'] == A)]['barrier (kcal/mol)'].min()
    min_barriers['BintersectAB'] = curr_df[(curr_df['status'] == 'intersectAB') & (curr_df['sim'] == B)]['barrier (kcal/mol)'].min()

    barriers = []
    diffs = []
    for ids in intersectAB:
        barrier_A = curr_df[(curr_df['sim'] == A) & (curr_df['run_ids'] == ids)]['barrier (kcal/mol)']
        barrier_B = curr_df[(curr_df['sim'] == B) & (curr_df['run_ids'] == ids)]['barrier (kcal/mol)']
        #print(barrier_A.values[0],barrier_B.values[0],barrier_A.values[0] - barrier_B.values[0])
        #if barrier_B.values[0] < 40:
        diffs.append(barrier_A.values[0] - barrier_B.values[0])
        barriers.append(barrier_B.values[0])
    MAE = np.mean(np.absolute(diffs))

    # Plot using seaborn's violinplot
    plt.figure(figsize=(width*0.38, width*0.35))
    ax = sns.violinplot(x='status', y='barrier (kcal/mol)', hue='sim',split=True,order= ['diffA','intersectAB','diffB'], palette=c_vals,data=curr_df,inner=None,legend=False)
    sns.stripplot(x='status', y='barrier (kcal/mol)', hue='sim', data=curr_df, order= ['diffA','intersectAB','diffB'],jitter=0.1, color='k', alpha=0.15, dodge=True, ax=ax,legend=False,size=2)
    plt.xlabel('Occurrence of Samples')
    plt.ylabel('Barrier of Mean Rate [kcal/mol]')
    #plt.title(f'Simulation A:{A} and B:{B}')

    plt.xticks([0,1,2],[f'{A} only','both datasets',f'{B} only',])

    plt.ylim((15,140))

    plt.text(-0.45,123,f"count:",fontsize=6)
    plt.text(0.1,123,f"{len(A_minus_B)}",fontsize=6)
    plt.text(0.92,123,f"{len(intersectAB)}",fontsize=6)
    plt.text(2.2,123,f"{len(B_minus_A)}",fontsize=6)


    plt.text(-0.45,128,f"min:",fontsize=6)
    plt.text(0.1,128,f"{min_barriers['diffA']:.1f}",fontsize=6)
    plt.text(0.7,128,f"{min_barriers['AintersectAB']:.1f}",fontsize=6)
    plt.text(1.2,128,f"{min_barriers['BintersectAB']:.1f}",fontsize=6)
    plt.text(2.2,128,f"{min_barriers['diffB']:.1f}",fontsize=6)

    plt.text(-0.45,133,f"MAE:",fontsize=6)
    plt.text(0.92,133,f"{MAE:.2f}",fontsize=6)
    plt.tight_layout()
    plt.savefig(plot_dir / f"sampling-paper-violin-diff-{A}-{B}-{data_transform}.png",dpi=300)

    # plt.figure(figsize=(10, 6))
    # plt.scatter(barriers,np.absolute(diffs))
    # plt.xlabel('Mean Rate Barrier of Longer Simulation [kcal/mol]')
    # plt.ylabel('Absolute Difference [kcal/mol]')
    # plt.title(f'Barrier-difference relation for simulation A:{A} and B:{B}')

    # plt.ylim((-1,40))
    # plt.savefig(plot_dir / f"sampling-production-barrier-difference_{data_transform}.png",dpi=300)
# %%
