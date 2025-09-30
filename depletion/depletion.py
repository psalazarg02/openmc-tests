import math
import openmc

#Create materials for single fuel pin
fuel = openmc.Material(name="uo2")
fuel.add_element("U", 1, percent_type="ao", enrichment=4.25)
fuel.add_element("O", 2)
fuel.set_density("g/cc", 10.4)

clad = openmc.Material(name="clad")
clad.add_element("Zr", 1)
clad.set_density("g/cc", 6)

water = openmc.Material(name="water")
water.add_element("O", 1)
water.add_element("H", 2)
water.set_density("g/cc", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")
materials = openmc.Materials([fuel, clad, water])

#Inner and Outer radius of fuel pin
radii = [0.42, 0.45]

#Create concentric cylinders and universe
pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
pin_univ = openmc.model.pin(pin_surfaces, materials)

#Define boundaries and materials of cylinders
bound_box = openmc.model.RectangularPrism(1.24, 1.24, boundary_type="reflective")
root_cell = openmc.Cell(fill=pin_univ, region=-bound_box)
geometry = openmc.Geometry([root_cell])

#geometry.root_universe.plot()

#Particle settings
settings = openmc.Settings()
settings.particles = 1000
settings.inactive = 10
settings.batches = 50

#Define volume as cross-sectional area of fuel
fuel.volume = math.pi * radii[0] ** 2

#Set up depletion
import openmc.deplete

#Simple chain, includes: I135, Xe135, Xe136, Cs135, Gd157, Gd156, U234, U235, U238
chain = openmc.deplete.Chain.from_xml("./chain_casl_pwr.xml")

#Create operator
model = openmc.Model(geometry=geometry, settings=settings)
operator = openmc.deplete.CoupledOperator(model, "./chain_casl_pwr.xml")

#Define fuel pin power/cm
power = 174

#Define depletion step size of 30 days
time_steps = [30] * 6

#Define integration and perform simulation
integrator = openmc.deplete.PredictorIntegrator(operator, 
                                                time_steps, 
                                                power, 
                                                timestep_units='d')

integrator.integrate()

#Extract results from simulations
results = openmc.deplete.Results("./depletion_results.h5")
time, k = results.get_keff()
time /= (24 * 60 * 60) #convert from seconds to days

#PLOTS
import matplotlib.pyplot as plt
_, u235 = results.get_atoms("1", "U235")
plt.plot(time, u235)
plt.xlabel("Time [d]")
plt.ylabel("Number of atoms - U235")
plt.savefig("depletion u235.png", format = "png")









