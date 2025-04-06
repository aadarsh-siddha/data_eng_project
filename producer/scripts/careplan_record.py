from typing import List, Dict


class CareplanRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.START= arr[1]
        self.STOP= arr[2]
        self.PATIENT= arr[3]
        self.ENCOUNTER= arr[4]
        self.CODE = int(arr[5]) if arr[5].strip() else None
        self.DESCRIPTION= arr[6]
        self.REASONCODE= int(arr[7]) if arr[7].strip() else None
        self.REASONDESCRIPTION= arr[8]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['Id'],
                d['START'],
                d['STOP'],
                d['PATIENT'],
                d['ENCOUNTER'],
                d['CODE'],
                d['DESCRIPTION'],
                d['REASONCODE'],
                d['REASONDESCRIPTION']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_careplan_record(obj, ctx):
    if obj is None:
        return None

    return CareplanRecord.from_dict(obj)


def careplan_record_to_dict(careplan_record: CareplanRecord, ctx):
    return careplan_record.__dict__