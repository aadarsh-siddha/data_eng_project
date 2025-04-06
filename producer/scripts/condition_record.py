from typing import List, Dict


class ConditionRecord:

    def __init__(self, arr: List[str]):
        self.START= arr[0]
        self.STOP= arr[1]
        self.PATIENT= arr[2]
        self.ENCOUNTER= arr[3]
        self.SYSTEM= arr[4]
        self.CODE = int(arr[5]) if arr[5].strip() else None
        self.DESCRIPTION= arr[6]
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['START'],
                d['STOP'],
                d['PATIENT'],
                d['ENCOUNTER'],
                d['SYSTEM'],
                d['CODE'],
                d['DESCRIPTION']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_condition_record(obj, ctx):
    if obj is None:
        return None

    return ConditionRecord.from_dict(obj)


def condition_record_to_dict(condition_record: ConditionRecord, ctx):
    return condition_record.__dict__