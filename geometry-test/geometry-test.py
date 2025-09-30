import matplotlib.pyplot as plt
import openmc

#Define materials
fuel = openmc.Material(name='fuel')
fuel.add_nuclide('U235', 1.0)
fuel.set_density('g/cm3', 10.0)

fuel2 = openmc.Material(name='fuel2')
fuel2.add_nuclide('U238', 1.0)
fuel2.set_density('g/cm3', 10.0)

water = openmc.Material(name='water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 1.0)

materials = openmc.Materials((fuel, fuel2, water))
materials.export_to_xml()


#Define universes
r_pin = openmc.ZCylinder(r=0.25)
fuel_cell = openmc.Cell(fill=fuel, region=-r_pin)
water_cell = openmc.Cell(fill=water, region=+r_pin)
pin_universe = openmc.Universe(cells=(fuel_cell, water_cell))

r_big_pin = openmc.ZCylinder(r=0.5)
fuel2_cell = openmc.Cell(fill=fuel2, region=-r_big_pin)
water2_cell = openmc.Cell(fill=water, region=+r_big_pin)
big_pin_universe = openmc.Universe(cells=(fuel2_cell, water2_cell))

all_water_cell = openmc.Cell(fill=water)
outer_universe = openmc.Universe(cells=(all_water_cell,))


#Create hexagonal lattice
lattice = openmc.HexLattice()
lattice.center = (0., 0.)
lattice.pitch = (1.25,)
lattice.outer = outer_universe

#Show rings working in lattice
#print(lattice.show_indices(num_rings=4))

#Build rings
outer_ring = [big_pin_universe] + [pin_universe]*17 # Adds up to 18

ring_1 = [big_pin_universe] + [pin_universe]*11 # Adds up to 12

ring_2 = [big_pin_universe] + [pin_universe]*5 # Adds up to 6

inner_ring = [big_pin_universe]

#Insert rings in lattice
lattice.universes = [outer_ring, 
                     ring_1, 
                     ring_2,
                     inner_ring]

#Show lattice
#print(lattice)


#Define geometry and export
outer_surface = openmc.ZCylinder(r=5.0, boundary_type='vacuum')
main_cell = openmc.Cell(fill=lattice, region=-outer_surface)
geometry = openmc.Geometry([main_cell])


#Define plot for geometry
plot = openmc.Plot.from_geometry(geometry)
plot.color_by = 'cell'
plot.colors = colors = {
    water: 'blue',
    fuel: 'olive', #U235
    fuel2: 'yellow' #U238
}

#Hexagonal geometry
main_cell.region = -openmc.model.HexagonalPrism(
    edge_length=4*lattice.pitch[0],
    orientation='x',
    boundary_type='vacuum'
)
lattice.orientation = 'x'
geometry.export_to_xml()

# Run OpenMC in plotting mode
plot.to_ipython_image()








