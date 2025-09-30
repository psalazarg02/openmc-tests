import matplotlib.pyplot as plt
import openmc 
import math

# Materials definitions

u235 = openmc.Material(name='U235')
u235.add_nuclide('U235', 1.0)
u235.set_density('g/cm3', 10.0)

u238 = openmc.Material(name='U238')
u238.add_nuclide('U238', 1.0)
u238.set_density('g/cm3', 10.0)

pu238 = openmc.Material(name='Pu238')
pu238.add_nuclide('Pu238', 1.0)
pu238.set_density('g/cm3', 10.0)

pu239 = openmc.Material(name='Pu239')
pu239.add_nuclide('Pu239', 1.0)
pu239.set_density('g/cm3', 10.0)

pu240 = openmc.Material(name='Pu240')
pu240.add_nuclide('Pu240', 1.0)
pu240.set_density('g/cm3', 10.0)

pu241 = openmc.Material(name='Pu241')
pu241.add_nuclide('Pu241', 1.0)
pu241.set_density('g/cm3', 10.0)

pu242 = openmc.Material(name='Pu242')
pu242.add_nuclide('Pu242', 1.0)
pu242.set_density('g/cm3', 10.0)

am241 = openmc.Material(name='Am241')
am241.add_nuclide('Am241', 1.0)
am241.set_density('g/cm3', 10.0)

o16 = openmc.Material(name='O16')
o16.add_nuclide('O16', 1.0)
o16.set_density('g/cm3', 10.0)

sodium_coolant = openmc.Material(name='Na')
sodium_coolant.add_nuclide('Na23', 1.0)
sodium_coolant.set_density('g/cm3', 0.96)

cu63 = openmc.Material(name='Cu63')
cu63.set_density('g/cm3', 10.0)
cu63.add_nuclide('Cu63', 1.0)

Al2O3 = openmc.Material(name='Al2O3')
Al2O3.set_density('g/cm3', 10.0)
Al2O3.add_element('O', 3.0)
Al2O3.add_element('Al', 2.0)


# Material mixtures
fuel = openmc.Material.mix_materials(
    [u235, u238, pu238, pu239, pu240, pu241, pu242, am241, o16],
    [0.0019, 0.7509, 0.0046, 0.0612, 0.0383, 0.0106, 0.0134, 0.001, 0.1181],
    'wo')

clad = openmc.Material.mix_materials(
    [cu63,Al2O3], [0.997,0.003], 'wo')

#Materials file
materials = openmc.Materials([fuel, clad, sodium_coolant])

#Define pincell geometry
radii = [0.42, 0.45]

#Create concentric cylinders and universe
pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
pin_univ = openmc.model.pin(pin_surfaces, materials)

#Define boundaries and materials of cylinders
bound_box = openmc.model.RectangularPrism(1.24, 1.24, boundary_type="reflective")
root_cell = openmc.Cell(fill=pin_univ, region=-bound_box)
geometry = openmc.Geometry([root_cell])

#Particle settings
settings = openmc.Settings()
settings.particles = 1000
settings.inactive = 10
settings.batches = 50

#Define volume as cross-sectional area of fuel
fuel.volume = math.pi * radii[0] ** 2

#Set up depletion
import openmc.deplete

#Simple chain fast spectrum
chain = openmc.deplete.Chain.from_xml("./chain_casl_sfr.xml")

#Create operator
model = openmc.Model(geometry=geometry, settings=settings)
operator = openmc.deplete.CoupledOperator(model, "./chain_casl_sfr.xml")

#Define fuel pin power/cm
power = 180

#Define depletion step size of 30 days
time_steps = [30] * 6

#Define integration and perform simulation
integrator = openmc.deplete.PredictorIntegrator(operator, 
                                                time_steps, 
                                                power, 
                                                timestep_units='d')

integrator.integrate()

