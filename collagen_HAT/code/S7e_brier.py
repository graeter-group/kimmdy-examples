# %%
from pathlib import Path
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

#%%
df_values= pd.read_csv(data_dir / "S7e_brier_data.csv",index_col=0)

#%%
plt.figure(figsize=(width*0.66,width*0.75))
for i, column in enumerate(df_values.columns):
    fraction_values = df_values[column]
    
    # Create boxplot for each column
    plt.boxplot(fraction_values, positions=[i], showfliers=False,
                boxprops=dict(linewidth=1), medianprops=dict(linewidth=1.5, color='k'), zorder=4)
    
    # Scatter plot for the same column values
    x_scatter = [i] * len(fraction_values)  # Position for scatter points
    plt.scatter(x_scatter, fraction_values, alpha=0.7, s=2)

# Set x-axis labels as column names
#plt.xticks(range(len(df_values.columns)), df_values.columns, rotation=30)
plt.xticks(range(3), ['all\nframes', '100 smallest\ntranslations','same\n probability'])

# Set labels for x and y axes
#plt.title('Probability distributions from a reduced set of frames vs ground truth (5ns 50 000frames)')
plt.ylabel('$d(q,p)$ [0,2]')

plt.tight_layout()
plt.savefig(plot_dir / f"brier_score_top100translation.png",dpi=300)
