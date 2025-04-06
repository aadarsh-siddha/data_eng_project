from typing import List, Dict


class ClaimRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.PATIENTID= arr[1]
        self.PROVIDERID= arr[2]
        self.PRIMARYPATIENTINSURANCEID= arr[3]
        self.SECONDARYPATIENTINSURANCEID= arr[4]
        self.DEPARTMENTID = int(arr[5]) if arr[5].strip() else None
        self.PATIENTDEPARTMENTID= int(arr[6]) if arr[6].strip() else None
        self.DIAGNOSIS1=int(arr[7]) if arr[7].strip() else None
        self.DIAGNOSIS2=int(arr[8]) if arr[8].strip() else None
        self.DIAGNOSIS3=int(arr[9]) if arr[9].strip() else None
        self.DIAGNOSIS4=int(arr[10]) if arr[10].strip() else None
        self.DIAGNOSIS5=int(arr[11]) if arr[11].strip() else None
        self.DIAGNOSIS6=int(arr[12]) if arr[12].strip() else None
        self.DIAGNOSIS7=int(arr[13]) if arr[13].strip() else None
        self.DIAGNOSIS8=int(arr[14]) if arr[14].strip() else None
        self.REFERRINGPROVIDERID= arr[15]
        self.APPOINTMENTID= arr[16]
        self.CURRENTILLNESSDATE= arr[17]
        self.SERVICEDATE= arr[18]
        self.SUPERVISINGPROVIDERID= arr[19]
        self.STATUS1= arr[20]
        self.STATUS2= arr[21]
        self.STATUSP= arr[22]
        self.OUTSTANDING1= float(arr[23]) if arr[23].strip() else None
        self.OUTSTANDING2= float(arr[24]) if arr[24].strip() else None
        self.OUTSTANDINGP= float(arr[25]) if arr[25].strip() else None
        self.LASTBILLDATE1= arr[26]
        self.LASTBILLDATE2= arr[27]
        self.LASTBILLDATEP= arr[28]
        self.HEALTHCARECLAIMTYPEID1= int(arr[29]) if arr[29].strip() else None
        self.HEALTHCARECLAIMTYPEID2= int(arr[30]) if arr[30].strip() else None
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
            d['Id'],
            d['PATIENTID'],
            d['PROVIDERID'],
            d['PRIMARYPATIENTINSURANCEID'],
            d['SECONDARYPATIENTINSURANCEID'],
            d['DEPARTMENTID'],
            d['PATIENTDEPARTMENTID'],
            d['DIAGNOSIS1'],
            d['DIAGNOSIS2'],
            d['DIAGNOSIS3'],
            d['DIAGNOSIS4'],
            d['DIAGNOSIS5'],
            d['DIAGNOSIS6'],
            d['DIAGNOSIS7'],
            d['DIAGNOSIS8'],
            d['REFERRINGPROVIDERID'],
            d['APPOINTMENTID'],
            d['CURRENTILLNESSDATE'],
            d['SERVICEDATE'],
            d['SUPERVISINGPROVIDERID'],
            d['STATUS1'],
            d['STATUS2'],
            d['STATUSP'],
            d['OUTSTANDING1'],
            d['OUTSTANDING2'],
            d['OUTSTANDINGP'],
            d['LASTBILLDATE1'],
            d['LASTBILLDATE2'],
            d['LASTBILLDATEP'],
            d['HEALTHCARECLAIMTYPEID1'],
            d['HEALTHCARECLAIMTYPEID2']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_claim_record(obj, ctx):
    if obj is None:
        return None

    return ClaimRecord.from_dict(obj)


def claim_record_to_dict(claim_record: ClaimRecord, ctx):
    return claim_record.__dict__