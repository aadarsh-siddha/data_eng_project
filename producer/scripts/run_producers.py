import subprocess
import os
def run_producers():
    resources = [
            'allergies',
            'careplans',
            'claims',
            'claims_transactions',
            'conditions',
            'devices',
            'encounters',
            'imaging_studies',
            'immunizations',
            'medications',
            'observations',
            'organizations',
            'patients',
            'payer_transitions',
            'payers',
            'procedures',
            'providers',
            'supplies'
        ]
    os.chdir('/app/scripts')
    for resource in resources:
        subprocess.run([
            "python", "resource_producer.py",
            "--csv", "../synthea/output/csv",
            "--schema", "../resources/schemas",
            "--class_path", "patient_record.py",
            "--config", "../config/kafka_config.json",
            "--resource", resource
        ])

if __name__ == "__main__":
    run_producers()
    