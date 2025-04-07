import os
import time
import subprocess
from pathlib import Path
from scripts.run_producers import run_producers

state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", 
               "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho",
               "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", 
               "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", 
               "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", 
               "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
               "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

SYNTHEA_STATUS = True
POPULATION = 20
SLEEP_TIME = 1800
base_path = Path("/app/synthea")

while(1):
    for state in state_names:
        if SYNTHEA_STATUS:
            os.chdir(base_path)
    
            output_path = base_path / "output"
            if output_path.exists():
                subprocess.run(['rm', '-r', str(output_path)], check=True)
    
            print(f"Generating data for {state}")
            subprocess.run(['./run_synthea', '-p', str(POPULATION), state,
                            '--exporter.fhir.export=false',
                            '--exporter.csv.export=true'], check=True)
    
            run_producers()
            print(f"Sleeping for {SLEEP_TIME} seconds...\n")
            time.sleep(SLEEP_TIME)
