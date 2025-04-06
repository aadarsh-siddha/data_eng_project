from typing import List, Dict


class OrganizationRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.NAME= arr[1]
        self.ADDRESS= arr[2]
        self.CITY= arr[3]
        self.STATE= arr[4]
        self.ZIP = int( arr[5]) if  arr[5].strip() else None
        self.LAT= float(arr[6]) if arr[6].strip() else None
        self.LON= float(arr[7]) if arr[7].strip() else None
        self.PHONE= int(arr[8]) if arr[8].strip() else None
        self.REVENUE=  float(arr[9]) if arr[9].strip() else None
        self.UTILIZATION= int(arr[10]) if arr[10].strip() else None
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['Id'],
                    d['NAME'],
                    d['ADDRESS'],
                    d['CITY'],
                    d['STATE'],
                    d['ZIP'],
                    d['LAT'],
                    d['LON'],
                    d['PHONE'],
                    d['REVENUE'],
                    d['UTILIZATION']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_organization_record(obj, ctx):
    if obj is None:
        return None

    return OrganizationRecord.from_dict(obj)


def organization_record_to_dict(organization_record: OrganizationRecord, ctx):
    return organization_record.__dict__