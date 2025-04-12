from typing import List, Dict


class Claims_transactionRecord:

    def __init__(self, arr: List[str]):
        self.ID= arr[0]
        self.CLAIMID= arr[1]
        self.CHARGEID= int(arr[2])
        self.PATIENTID= arr[3]
        self.TYPE= arr[4]
        self.AMOUNT = float(arr[5]) if arr[5].strip() else None
        self.METHOD= arr[6]
        self.FROMDATE= arr[7]
        self.TODATE= arr[8]
        self.PLACEOFSERVICE= arr[9]
        self.PROCEDURECODE= int(arr[10]) if arr[10].strip() else None
        self.MODIFIER1= arr[11]
        self.MODIFIER2= arr[12]
        self.DIAGNOSISREF1= int(arr[13]) if arr[13].strip() else None
        self.DIAGNOSISREF2= int(arr[14]) if arr[14].strip() else None
        self.DIAGNOSISREF3= int(arr[15]) if arr[15].strip() else None
        self.DIAGNOSISREF4= int(arr[16]) if arr[16].strip() else None
        self.UNITS= int(arr[17]) if arr[17].strip() else None
        self.DEPARTMENTID= int(arr[18]) if arr[18].strip() else None
        self.NOTES= arr[19]
        self.UNITAMOUNT= float(arr[20]) if arr[20].strip() else None
        self.TRANSFEROUTID= int(arr[21]) if arr[21].strip() else None
        self.TRANSFERTYPE= arr[22]
        self.PAYMENTS= float(arr[23]) if arr[23].strip() else None
        self.ADJUSTMENTS= float(arr[24]) if arr[24].strip() else None
        self.TRANSFERS= float(arr[25]) if arr[25].strip() else None
        self.OUTSTANDING= float(arr[26]) if arr[26].strip() else None
        self.APPOINTMENTID= arr[27]
        self.LINENOTE= arr[28]
        self.PATIENTINSURANCEID= arr[29]
        self.FEESCHEDULEID= int(arr[30]) if arr[30].strip() else None
        self.PROVIDERID= arr[31]
        self.SUPERVISINGPROVIDERID= arr[32]
        
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['ID'],
                d['CLAIMID'],
                d['CHARGEID'],
                d['PATIENTID'],
                d['TYPE'],
                d['AMOUNT'],
                d['METHOD'],
                d['FROMDATE'],
                d['TODATE'],
                d['PLACEOFSERVICE'],
                d['PROCEDURECODE'],
                d['MODIFIER1'],
                d['MODIFIER2'],
                d['DIAGNOSISREF1'],
                d['DIAGNOSISREF2'],
                d['DIAGNOSISREF3'],
                d['DIAGNOSISREF4'],
                d['UNITS'],
                d['DEPARTMENTID'],
                d['NOTES'],
                d['UNITAMOUNT'],
                d['TRANSFEROUTID'],
                d['TRANSFERTYPE'],
                d['PAYMENTS'],
                d['ADJUSTMENTS'],
                d['TRANSFERS'],
                d['OUTSTANDING'],
                d['APPOINTMENTID'],
                d['LINENOTE'],
                d['PATIENTINSURANCEID'],
                d['FEESCHEDULEID'],
                d['PROVIDERID'],
                d['SUPERVISINGPROVIDERID']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_claims_transaction_record(obj, ctx):
    if obj is None:
        return None

    return Claims_transactionRecord.from_dict(obj)


def claims_transaction_record_to_dict(claims_transaction_record: Claims_transactionRecord, ctx):
    return claims_transaction_record.__dict__