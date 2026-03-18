#%%
import numpy as np
import pandas as pd

for i in ['a', 'b', 'c', 'd']:
    # Read the .dat file
    data = np.loadtxt(f'severalEPR_SI{i}.dat')
    
    # Convert numpy array to DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to CSV
    df.to_csv(f'severalEPR_SI{i}.csv', index=False)

# %%
