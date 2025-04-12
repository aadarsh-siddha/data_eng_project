from typing import List, Dict


class PatientRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.BIRTHDATE= arr[1]
        self.DEATHDATE= arr[2]
        self.SSN= arr[3]
        self.DRIVERS= arr[4]
        self.PASSPORT = arr[5]
        self.PREFIX= arr[6]
        self.FIRST= arr[7]
        self.MIDDLE= arr[8]
        self.LAST= arr[9]
        self.SUFFIX= arr[10]
        self.MAIDEN= arr[11]
        self.MARITAL= arr[12]
        self.RACE= arr[13]
        self.ETHINICITY= arr[14]
        self.GENDER= arr[15]
        self.BIRTHPLACE= arr[16]
        self.ADDRESS= arr[17]
        self.CITY= arr[18]
        self.STATE= arr[19]
        self.COUNTY= arr[20]
        self.FIPS= int(arr[21]) if arr[21].strip() else None
        self.ZIP= int(arr[22]) if arr[22].strip() else None
        self.LAT= float(arr[23]) if arr[23].strip() else None
        self.LON= float(arr[24]) if arr[24].strip() else None
        self.HEALTHCARE_EXPENSES= float(arr[25]) if arr[25].strip() else None
        self.HEALTHCARE_COVERAGE= float(arr[26]) if arr[26].strip() else None
        self.INCOME= int(arr[27]) if arr[27].strip() else None
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['Id'], 
                    d['BIRTHDATE'], 
                    d['DEATHDATE'], 
                    d['SSN'], 
                    d['DRIVERS'],  
                    d['PASSPORT'], 
                    d['PREFIX'],
                    d['FIRST'],
                    d['MIDDLE'],
                    d['LAST'],
                    d['SUFFIX'],
                    d['MAIDEN'],
                    d['MARITAL'],
                    d['RACE'],
                    d['ETHINICITY'],
                    d['GENDER'],
                    d['BIRTHPLACE'],
                    d['ADDRESS'],
                    d['CITY'],
                    d['STATE'],
                    d['COUNTY'],
                    d['FIPS'],
                    d['ZIP'],
                    d['LAT'],
                    d['LON'],
                    d['HEALTHCARE_EXPENSES'],
                    d['HEALTHCARE_COVERAGE'],
                    d['INCOME']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_patient_record(obj, ctx):
    if obj is None:
        return None

    return PatientRecord.from_dict(obj)


def patient_record_to_dict(patient_record: PatientRecord, ctx):
    return patient_record.__dict__