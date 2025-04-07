from typing import List, Dict


class ProviderRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.ORGANIZATION= arr[1]
        self.NAME= arr[2]
        self.GENDER= arr[3]
        self.SPECIALITY= arr[4]
        self.ADDRESS = arr[5]
        self.CITY= arr[6]
        self.STATE = arr[7]
        self.ZIP= int(arr[8]) if arr[8].strip() else None
        self.LAT= float(arr[9]) if arr[9].strip() else None
        self.LON= float(arr[10]) if arr[10].strip() else None
        self.ENCOUNTERS= int(arr[11]) if arr[11].strip() else None
        self.PROCEDURES= int(arr[12]) if arr[12].strip() else None

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['Id'],
                    d['ORGANIZATION'],
                    d['NAME'],
                    d['GENDER'],
                    d['SPECIALITY'],
                    d['ADDRESS'],
                    d['CITY'],
                    d['STATE'],
                    d['ZIP'],
                    d['LAT'],
                    d['LON'],
                    d['ENCOUNTERS'],
                    d['PROCEDURES']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_provider_record(obj, ctx):
    if obj is None:
        return None

    return ProviderRecord.from_dict(obj)


def provider_record_to_dict(provider_record: ProviderRecord, ctx):
    return provider_record.__dict__