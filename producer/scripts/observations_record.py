from typing import List, Dict


class ObservationRecord:

    def __init__(self, arr: List[str]):
        self.DATE= arr[0]
        self.PATIENT= arr[1]
        self.ENCOUNTER= arr[2]
        self.CATEGORY= arr[3]
        self.CODE= arr[4]
        self.DESCRIPTION = arr[5]
        self.VALUE= arr[6]
        self.UNITS= arr[7]
        self.TYPE= arr[8]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['DATE'],
                    d['PATIENT'],
                    d['ENCOUNTER'],
                    d['CATEGORY'],
                    d['CODE'],
                    d['DESCRIPTION'],
                    d['VALUE'],
                    d['UNITS'],
                    d['TYPE']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_observation_record(obj, ctx):
    if obj is None:
        return None

    return ObservationRecord.from_dict(obj)


def observation_record_to_dict(observation_record: ObservationRecord, ctx):
    return observation_record.__dict__