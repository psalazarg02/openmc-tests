import openmc
import openmc.deplete
import matplotlib.pyplot as plt
from pathlib import Path
import os

#Extract results from simulations
custom_path = "./simulation_results01/depletion_results.h5"
results = openmc.deplete.Results(custom_path)
time, k = results.get_keff()
time /= (24 * 60 * 60) #convert from seconds to days
_, pu238 = results.get_atoms('13', nuc='Pu238')
_, pu239 = results.get_atoms('13', nuc='Pu239')
_, pu240 = results.get_atoms('13', nuc='Pu240')
_, pu241 = results.get_atoms('13', nuc='Pu241')
_, u238 = results.get_atoms('13', nuc='U238')
_, u239 = results.get_atoms('13', nuc='U239')
_, am241 = results.get_atoms('13', nuc='Am241')


#Create isotope dictionary for plot
isotopes = {
    'u238': u238,
    'u239': u239, 
    'pu238': pu238,
    'pu239': pu239,
    'pu240': pu240,
    'pu241': pu241,
    'am241': am241
}

def new_folder(base_name):
    """Create a new folder with an incremental suffix"""
    suffix = 1
    while True:
        folder_name = f'{base_name}{suffix:02d}'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return folder_name
        suffix += 1

#Create a new unique results directory
folder_name = new_folder('depletion_results')
results_dir = Path(folder_name)

#Plot and save in depletion_results folder
for name, data in isotopes.items():
    print("Creating plot for", name)
    plt.figure()
    plt.plot(time, data)
    plt.xlabel("Time [d]")
    plt.ylabel(f"Number of atoms - {name.upper()}")

# Save to depletion_results folder
    filename = f"depletion_{name}.png"
    filepath = results_dir / filename
    plt.savefig(filepath, format="png", bbox_inches='tight')
    plt.close()

