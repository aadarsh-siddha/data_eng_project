from typing import List, Dict


class Payer_transitionRecord:

    def __init__(self, arr: List[str]):
        self.PATIENT= arr[0]
        self.MEMBERID= arr[1]
        self.START_DATE= arr[2]
        self.END_DATE= arr[3]
        self.PAYER= arr[4]
        self.SECONDARY_PAYER = arr[5]
        self.PLAN_OWNERSHIP= arr[6]
        self.OWNER_NAME= arr[7]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['PATIENT'],
                d['MEMBERID'],
                d['START_DATE'],
                d['END_DATE'],
                d['PAYER'],
                d['SECONDARY_PAYER'],
                d['PLAN_OWNERSHIP'],
                d['OWNER_NAME']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_payer_transition_record(obj, ctx):
    if obj is None:
        return None

    return Payer_transitionRecord.from_dict(obj)


def payer_transition_record_to_dict(_record: Payer_transitionRecord, ctx):
    return _record.__dict__