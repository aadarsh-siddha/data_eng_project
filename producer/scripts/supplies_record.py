from typing import List, Dict


class SuppliesRecord:

    def __init__(self, arr: List[str]):
        self.DATE= arr[0]
        self.PATIENT= arr[1]
        self.ENCOUNTER= arr[2]
        self.CODE= int(arr[3]) if arr[3].strip() else None
        self.DESCRIPTION= arr[4]
        self.QUANTITY = int(arr[5]) if arr[5].strip() else None

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['DATE'],
                    d['PATIENT'],
                    d['ENCOUNTER'],
                    d['CODE'],
                    d['DESCRIPTION'],
                    d['QUANTITY']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_supplies_record(obj, ctx):
    if obj is None:
        return None

    return SuppliesRecord.from_dict(obj)


def supplies_record_to_dict(supplies_record: SuppliesRecord, ctx):
    return supplies_record.__dict__