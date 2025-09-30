import openmc
import openmc.deplete
import matplotlib.pyplot as plt

#Extract results from simulations
results = openmc.deplete.Results("./depletion_results.h5")
time, pu239 = results.get_atoms('13', nuc='Pu239')
time /= (24 * 60 * 60) #convert from seconds to days

plt.plot(time, pu239)
plt.xlabel("Time [d]")
plt.ylabel("Number of atoms - Pu239")
plt.savefig("depletion pu239.png", format = "png")

"""
time, nucs = results[0]
time /= (24 * 60 * 60) #convert from seconds to days

pu239 = nucs[1].get('Pu239', 0)

#PLOTS
plt.plot(time, pu239)
plt.xlabel("Time [d]")
plt.ylabel("Number of atoms - Pu239")
plt.savefig("depletion pu239.png", format = "png")
"""