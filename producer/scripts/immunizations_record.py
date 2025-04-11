from typing import List, Dict


class ImmunizationRecord:

    def __init__(self, arr: List[str]):
        self.DATE = arr[0]
        self.PATIENT = arr[1]
        self.ENCOUNTER = arr[2]
        self.CODE = int(arr[3]) if arr[3].strip() else None
        self.DESCRIPTION = arr[4]
        self.BASE_COST = float(arr[5]) if arr[5].strip() else None
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['DATE'],
                d['PATIENT'],
                d['ENCOUNTER'],
                d['CODE'],
                d['DESCRIPTION'],
                d['BASE_COST']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_immunization_record(obj, ctx):
    if obj is None:
        return None

    return ImmunizationRecord.from_dict(obj)


def immunization_record_to_dict(immunization_record: ImmunizationRecord, ctx):
    return immunization_record.__dict__