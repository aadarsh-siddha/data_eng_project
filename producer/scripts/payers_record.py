from typing import List, Dict


class PayerRecord:

    def __init__(self, arr: List[str]):
        self.Id= arr[0]
        self.NAME= arr[1]
        self.OWNERSHIP= arr[2]
        self.ADDRESS= arr[3]
        self.CITY= arr[4]
        self.STATE_HEADQUARTERS = arr[5]
        self.ZIP= int(arr[6]) if arr[6].strip() else None
        self.PHONE= int(arr[7]) if arr[7].strip() else None
        self.AMOUNT_COVERED= float(arr[8]) if arr[8].strip() else None
        self.AMOUNT_UNCOVERED= float(arr[9]) if arr[9].strip() else None
        self.REVENUE= float(arr[10]) if arr[10].strip() else None
        self.COVERED_ENCOUNTERS= int(arr[11]) if arr[11].strip() else None
        self.UNCOVERED_ENCOUNTERS= int(arr[12]) if arr[12].strip() else None
        self.COVERED_MEDICATIONS= int(arr[13]) if arr[13].strip() else None
        self.UNCOVERED_MEDICATIONS= int(arr[14]) if arr[14].strip() else None
        self.COVRED_PROCEDURES= int(arr[15]) if arr[15].strip() else None
        self.UNCOVRED_PROCEDURES= int(arr[16]) if arr[16].strip() else None
        self.COVERED_IMMUNIZATIONS= int(arr[17]) if arr[17].strip() else None
        self.UNCOVRED_IMMUNIZATIONS= int(arr[18]) if arr[18].strip() else None
        self.UNIQUE_CUSTOMERS= int(arr[19]) if arr[19].strip() else None
        self.QOLS_AVERAGE= float(arr[20]) if arr[20].strip() else None
        self.MEMBER_MONTHS= int(arr[21]) if arr[21].strip() else None
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                    d['Id'],
                    d['NAME'],
                    d['OWNERSHIP'],
                    d['ADDRESS'],
                    d['CITY'],
                    d['STATE_HEADQUARTERS'],
                    d['ZIP'],
                    d['PHONE'],
                    d['AMOUNT_COVERED'],
                    d['AMOUNT_UNCOVERED'],
                    d['REVENUE'],
                    d['COVERED_ENCOUNTERS'],
                    d['UNCOVERED_ENCOUNTERS'],
                    d['COVERED_MEDICATIONS'],
                    d['UNCOVERED_MEDICATIONS'],
                    d['COVRED_PROCEDURES'],
                    d['UNCOVRED_PROCEDURES'],
                    d['COVERED_IMMUNIZATIONS'],
                    d['UNCOVRED_IMMUNIZATIONS'],
                    d['UNIQUE_CUSTOMERS'],
                    d['QOLS_AVERAGE'],
                    d['MEMBER_MONTHS']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_payer_record(obj, ctx):
    if obj is None:
        return None

    return PayerRecord.from_dict(obj)


def payer_record_to_dict(payer_record: PayerRecord, ctx):
    return payer_record.__dict__