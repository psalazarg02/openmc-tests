import openmc
import matplotlib.pyplot as plt

# Create plutonium metal material
pu = openmc.Material()
pu.set_density('sum')
pu.add_nuclide('Pu239', 3.7047e-02)
pu.add_nuclide('Pu240', 1.7512e-03)
pu.add_nuclide('Pu241', 1.1674e-04)
pu.add_element('Ga', 1.3752e-03)
mats = openmc.Materials([pu])
mats.export_to_xml()

# Create a single cell filled with the Pu metal
sphere = openmc.Sphere(r=6.3849, boundary_type='vacuum')
cell = openmc.Cell(fill=pu, region=-sphere)
geom = openmc.Geometry([cell])
geom.export_to_xml()

# Set up energy spectrum tally
energy_bins = openmc.mgxs.GROUP_STRUCTURES['CCFE-709']
energy_filter = openmc.EnergyFilter(energy_bins)

spectrum_tally = openmc.Tally(name='energy_spectrum')
spectrum_tally.filters = [energy_filter]
spectrum_tally.scores = ['flux']

# Create tallies and export
tallies = openmc.Tallies([spectrum_tally])
tallies.export_to_xml()

# Finally, define some run settings
settings = openmc.Settings()
settings.batches = 200
settings.inactive = 10
settings.particles = 10000
settings.export_to_xml()

# Run the simulation
openmc.run()

# Get the resulting k-effective value and plot spectrum
n = settings.batches
with openmc.StatePoint(f'statepoint.{n}.h5') as sp:
    keff = sp.keff
    print(f'Final k-effective = {keff}')
    
    # Get the tally by name
    spectrum_tally = sp.get_tally(name='energy_spectrum')
    
    # Plot energy spectrum
    plt.figure(figsize=(10, 6))
    energies = energy_bins[:-1]  # Use lower bin edges
    flux_vals = spectrum_tally.mean.flatten()
    
    plt.step(energies, flux_vals, where='pre')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Energy (eV)')
    plt.ylabel('Flux per lethargy')
    plt.title('Neutron Energy Spectrum in Plutonium Sphere')
    plt.grid(True, alpha=0.3)
    
    # Save the plot instead of showing it
    plt.savefig('neutron_spectrum.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'neutron_spectrum.png' and 'neutron_spectrum.pdf'")