echo "Starting OpenMC depletion simulation..."
echo "Output will be saved in: simulation_resultsXX/"

#Record start time
start_time=$(date +%s)

#Generate materials file
echo "Running materials.py..."
python materials.py

#Generate geometry file  
echo "Running geometry.py..."
python geometry.py

#Generate settings file
echo "Running settings.py..."
python settings.py

#Run depletion simulation
echo "Running depletion.py..."
python depletion.py

#Calculate elapsed time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Simulation completed!"
echo "Total execution time: $((elapsed / 3600))h $(( (elapsed % 3600) / 60 ))m $((elapsed % 60))s"