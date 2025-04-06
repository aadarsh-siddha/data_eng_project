from typing import List, Dict


class Imaging_Study_Record:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.DATE= arr[1]
        self.PATIENT= arr[2]
        self.ENCOUNTER= arr[3]
        self.SERIES_UID= arr[4]
        self.BODYSITECODE = int(arr[5]) if arr[5].strip() else None
        self.BODYSITEDESCRIPTION= arr[6]
        self.MODALITYCODE= arr[7]
        self.MODALITYDESCRIPTION= arr[8]
        self.INSTANCE_UID= arr[9]
        self.SOP_CODE= arr[10]
        self.SOP_DESCRIPTION= arr[11]
        self.PROCEDURECODE= int(arr[12]) if arr[12].strip() else None
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['Id'],
                d['DATE'],
                d['PATIENT'],
                d['ENCOUNTER'],
                d['SERIES_UID'],
                d['BODYSITECODE'],
                d['BODYSITEDESCRIPTION'],
                d['MODALITYCODE'],
                d['MODALITYDESCRIPTION'],
                d['INSTANCE_UID'],
                d['SOP_CODE'],
                d['SOP_DESCRIPTION'],
                d['PROCEDURECODE']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_imaging_study_record(obj, ctx):
    if obj is None:
        return None

    return Imaging_Study_Record.from_dict(obj)


def imaging_study_record_to_dict(imaging_study_record: Imaging_Study_Record, ctx):
    return imaging_study_record.__dict__