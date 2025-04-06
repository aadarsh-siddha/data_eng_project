from typing import List, Dict


class MedicationRecord:

    def __init__(self, arr: List[str]):
        self.START= arr[0]
        self.STOP= arr[1]
        self.PATIENT= arr[2]
        self.PAYER= arr[3]
        self.ENCOUNTER= arr[4]
        self.CODE = int(arr[5]) if arr[5].strip() else None
        self.DESCRIPTION= arr[6]
        self.BASE_COST= float(arr[7]) if arr[7].strip() else None
        self.PAYER_COVERAGE= float(arr[8]) if arr[8].strip() else None
        self.DISPENSES= int(arr[9]) if arr[9].strip() else None
        self.TOTAL_COST= float(arr[10]) if arr[10].strip() else None
        self.REASONCODE= int(arr[11]) if arr[11].strip() else None
        self.REASONDESCRIPTION= arr[12]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['START'],
                d['STOP'],
                d['PATIENT'],
                d['PAYER'],
                d['ENCOUNTER'],
                d['CODE'],
                d['DESCRIPTION'],
                d['BASE_COST'],
                d['PAYER_COVERAGE'],
                d['DISPENSES'],
                d['TOTAL_COST'],
                d['REASONCODE'],
                d['REASONDESCRIPTION']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_medication_record(obj, ctx):
    if obj is None:
        return None

    return MedicationRecord.from_dict(obj)


def medication_record_to_dict(medication_record: MedicationRecord, ctx):
    return medication_record.__dict__