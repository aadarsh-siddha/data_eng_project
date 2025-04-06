from typing import Dict


class PatientRecordKey:
    def __init__(self):
        self.key = "patient"

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(key=d['patient'])

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_patient_record_key(obj, ctx):
    if obj is None:
        return None

    return PatientRecordKey.from_dict(obj)


def patient_record_key_to_dict(patient_record_key: PatientRecordKey, ctx):
    return patient_record_key.__dict__