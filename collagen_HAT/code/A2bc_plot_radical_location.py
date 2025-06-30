#%%
from pathlib import Path
import numpy as np
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import MDAnalysis as mda

#%%
import kimmdy_paper_theme
plot_colors = kimmdy_paper_theme.auto_init()
width = kimmdy_paper_theme.double_column

#%%
cwd = Path("/hits/fast/mbm/hartmaec/workdir/collagen_HAT/paper-figures/")
plot_dir = cwd / "plots"
data_dir = cwd / "data" / "extended_data"

# %%
reaction_atoms = dict(np.load(data_dir/ "A2bc_reaction_atoms.npz",allow_pickle=True))
reaction_atoms = {k:v.flatten()[0] for k,v in reaction_atoms.items()}

# %%
num_reactions = []
n_reactions_simids = {i:[] for i in range(21)}
for k,v in reaction_atoms.items():
    print(k,len(v))
    num_reactions.append(len(v))
    n_reactions_simids[len(v)].append(k)
print(f"{sum(num_reactions)} reactions!")

# %%
u = mda.Universe((data_dir / "A2bc_sample.tpr").as_posix(),(data_dir / "A2bc_sample.gro").as_posix())
u.atoms.ids = u.atoms.indices + 1

# %%
radicals = {}
for k,v in reaction_atoms.items():
    for kv,vv in v.items():
        if radicals.get(vv[0],None) is None:
            radicals[vv[0]] = 0
        radicals[vv[0]] += 1
        if vv[0] == '57019':
            print(k,v)
# %%
backbone = 0
sidechain = 0
crosslink = 0
aa_counter = Counter()
dopa_r_ids = []
LYX_r_ids = []
for k,v in radicals.items():
    print(k,v)
    a = u.select_atoms(f"id {k}")[0]
    aa_counter[a.resname] +=v

    if a.resname in ['L4Y','L5Y','LY2','LY3','LYX']:
        print(a)
        if a.resname == 'LYX':
            LYX_r_ids.append(k)
        crosslink += v
        continue
    if a.name in ['C','O','N','CA']:
        #print(a)
        backbone += v
    else:
        #print(a)
        sidechain += v
    if a.resname in ['TYR','DOP','PHE','DO1','DO2']:
        print('!!!!!!!!!!!')
        print(k,v)
        dopa_r_ids.append(k)
        print('!!!!!!!!!!!')

# %%
palette = sns.color_palette('pastel')
plt.figure(figsize=(width*0.33,width*0.3))
plt.bar(['back-\nbone','side\nchain','cross-\nlink'],[backbone,sidechain,crosslink],color=palette[7])
plt.ylabel('Reaction count')
plt.tight_layout()
plt.savefig(plot_dir / "radical_bb_sc_cl.png",dpi=300)


# %%
import networkx as nx
from networkx import NetworkXNoPath
from tqdm import tqdm
#%%
G = nx.Graph()
for bond in tqdm(u.bonds):
    G.add_edge(bond[0].id, bond[1].id)  

# %%
classifications = Counter()
    
for key, atoms in reaction_atoms.items():
    
    for atom_id, atom_tuple in atoms.items():
        atom1, atom2, atom3 = atom_tuple

        try:
            n_edges = len(nx.shortest_path(G,int(atom1),int(atom3)))
            classifications[n_edges] += 1
        except NetworkXNoPath:
            classifications[0] +=1

# %%
HAT_type = {'intermolecular':0,'>1-6':0}
for k,v in classifications.items():
    if k == 0:
        HAT_type['intermolecular'] = v
    elif k > 6:
        HAT_type['>1-6'] += v
    elif k > 0 and k <= 6:
        HAT_type[f"1-{k}"] = v
    else:
        raise ValueError(k)

#%%
HAT_type = {k:HAT_type[k] for k in sorted(HAT_type.keys())}

#%%
keys = [ str(x) for x in HAT_type.keys()]
keys[-1] = f'inter-\nmolecular'

# %%
palette = sns.color_palette('pastel')
plt.figure(figsize=(width*0.33,width*0.3))
plt.bar(HAT_type.keys(),HAT_type.values(),color=palette[7])
plt.xticks(range(7),keys)
#plt.xlabel('HAT Type')
plt.ylabel('Reaction count')
plt.tight_layout()
plt.savefig(plot_dir / "radical_transfer_number.png",dpi=300)
