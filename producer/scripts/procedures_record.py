from typing import List, Dict


class ProcedureRecord:

    def __init__(self, arr: List[str]):
        self.START= arr[0]
        self.STOP= arr[1]
        self.PATIENT= arr[2]
        self.ENCOUNTER= arr[3]
        self.SYSTEM= arr[4]
        self.CODE = int(arr[5]) if arr[5].strip() else None
        self.DESCRIPTION= arr[6]
        self.BASE_COST = arr[7]
        self.REASON_CODE= int(arr[8]) if arr[8].strip() else None
        self.REASON_DESCRIPTION= arr[9]

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['START'],
                    d['STOP'],
                    d['PATIENT'],
                    d['ENCOUNTER'],
                    d['SYSTEM'],
                    d['CODE'],
                    d['DESCRIPTION'],
                    d['BASE_COST'],
                    d['REASON_CODE'],
                    d['REASON_DESCRIPTION']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_procedure_record(obj, ctx):
    if obj is None:
        return None

    return ProcedureRecord.from_dict(obj)


def procedure_record_to_dict(procedure_record: ProcedureRecord, ctx):
    return procedure_record.__dict__