import openmc
from materials import create_materials

def create_geometry():
    materials, fuel = create_materials()
    
    # Define pincell geometry
    radii = [0.42, 0.45]

    # Create concentric cylinders and universe
    pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
    pin_univ = openmc.model.pin(pin_surfaces, materials)

    # Define boundaries and materials of cylinders
    bound_box = openmc.model.RectangularPrism(1.24, 1.24, boundary_type="reflective")
    root_cell = openmc.Cell(fill=pin_univ, region=-bound_box)
    geometry = openmc.Geometry([root_cell])
    
    return geometry, radii, fuel

if __name__ == "__main__":
    geometry, radii, fuel = create_geometry()