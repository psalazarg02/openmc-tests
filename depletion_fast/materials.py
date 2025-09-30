import openmc

def create_materials():
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

    # Materials file
    materials = openmc.Materials([fuel, clad, sodium_coolant])
    
    return materials, fuel

if __name__ == "__main__":
    materials, fuel = create_materials()