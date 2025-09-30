import openmc
import openmc.deplete
import math
import os
from geometry import create_geometry
from settings import create_settings

#Define function to create the results folders
def new_folder(base_name):
    suffix = 1
    while True:
        folder_name = f'{base_name}{suffix:02d}'
        if not os.path.exists(folder_name):
            return folder_name
        suffix += 1


def run_depletion():
    # Create output directory
    folder_name = new_folder('simulation_results')
    os.makedirs(folder_name)
    
    # Get geometry, settings, and fuel
    geometry, radii, fuel = create_geometry()
    settings = create_settings()
    
    # Define volume as cross-sectional area of fuel
    fuel.volume = math.pi * radii[0] ** 2

    # Set up depletion
    # Simple chain fast spectrum    
    chain = openmc.deplete.Chain.from_xml("./chain_casl_sfr.xml")

    # Create operator
    model = openmc.Model(geometry=geometry, settings=settings)
    operator = openmc.deplete.CoupledOperator(model, "./chain_casl_sfr.xml")

    # Define fuel pin power/cm
    power = 180

    # Define depletion step size of 30 days
    time_steps = [30] * 6

    # Define integration and perform simulation
    integrator = openmc.deplete.PredictorIntegrator(
        operator, 
        time_steps, 
        power, 
        timestep_units='d'
    )

    # Create full path for depletion results in the simulation folder
    results_path = os.path.join(folder_name, 'depletion_results.h5')

    print("Starting depletion simulation...")
    integrator.integrate(final_step=True, output=True, path=results_path)
    print(f"Depletion simulation completed! Results saved to: {results_path}")

if __name__ == "__main__":
    run_depletion()