import subprocess
import os
def run_producers():
    producers = [
            'allergies_producer.py',
            'careplan_producer.py',
            'claims_producer.py',
            'claims_transaction_producer.py',
            'condition_producer.py',
            'device_producer.py',
            'encounter_producer.py',
            'imaging_studies_producer.py',
            'immunizations_producer.py',
            'medications_producer.py',
            'observations_producer.py',
            'organizations_producer.py',
            'patient_producer.py',
            'payer_transitions_producer.py',
            'payers_producer.py',
            'procedures_producer.py',
            'providers_producer.py',
            'supplies_producer.py'
        ]
    os.chdir('/app/scripts')
    for producer in producers:
        subprocess.run(['python3',producer])

if __name__ == "__main__":
    run_producers()
    