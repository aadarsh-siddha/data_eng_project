from typing import List, Dict


class EncounterRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.START= arr[1]
        self.STOP= arr[2]
        self.PATIENT= arr[3]
        self.ORGANIZATION= arr[4]
        self.PROVIDER = arr[5]
        self.PAYER= arr[6]
        self.ENCOUNTERCLASS= arr[7]
        self.CODE= int(arr[8]) if arr[8].strip() else None
        self.DESCRIPTION= arr[9]
        self.BASE_ENCOUNTER_COST= float(arr[10]) if arr[10].strip() else None
        self.TOTAL_CLAIM_COST= float(arr[11]) if arr[11].strip() else None
        self.PAYER_COVERAGE= float(arr[12]) if arr[12].strip() else None
        self.REASONCODE= int(arr[13]) if arr[13].strip() else None
        self.REASONDESCRIPTION= arr[14]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['Id'],
                d['START'],
                d['STOP'],
                d['PATIENT'],
                d['ORGANIZATION'],
                d['PROVIDER'],
                d['PAYER'],
                d['ENCOUNTERCLASS'],
                d['CODE'],
                d['DESCRIPTION'],
                d['BASE_ENCOUNTER_COST'],
                d['TOTAL_CLAIM_COST'],
                d['PAYER_COVERAGE'],
                d['REASONCODE'],
                d['REASONDESCRIPTION']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_encounter_record(obj, ctx):
    if obj is None:
        return None

    return EncounterRecord.from_dict(obj)


def encounter_record_to_dict(encounter_record: EncounterRecord, ctx):
    return encounter_record.__dict__