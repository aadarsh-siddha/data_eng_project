from typing import List, Dict


class AllergiesRecord:

    def __init__(self, arr: List[str]):
        self.START= arr[0]
        self.STOP= arr[1]
        self.PATIENT= arr[2]
        self.ENCOUNTER= arr[3]
        self.CODE= int(arr[4])
        self.SYSTEM = arr[5]
        self.DESCRIPTION= arr[6]
        self.TYPE= arr[7]
        self.CATEGORY= arr[8]
        self.REACTION1= int(arr[9]) if arr[9].strip() else None
        self.DESCRIPTION1= arr[10]
        self.SEVERITY1= arr[11]
        self.REACTION2= int(arr[12]) if arr[12].strip() else None
        self.DESCRIPTION2= arr[13]
        self.SEVERITY2= arr[14]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['START'],
                d['STOP'],
                d['PATIENT'],
                d['ENCOUNTER'],
                d['CODE'],
                d['SYSTEM'], 
                d['DESCRIPTION'],
                d['TYPE'],
                d['CATEGORY'],
                d['REACTION1'],
                d['DESCRIPTION1'],
                d['SEVERITY1'],
                d['REACTION2'],
                d['DESCRIPTION2'],
                d['SEVERITY2'],
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_patient_record(obj, ctx):
    if obj is None:
        return None

    return AllergiesRecord.from_dict(obj)


def allergies_record_to_dict(allergies_record: AllergiesRecord, ctx):
    return allergies_record.__dict__