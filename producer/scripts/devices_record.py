from typing import List, Dict


class DeviceRecord:

    def __init__(self, arr: List[str]):
        self.START= arr[0]
        self.STOP= arr[1]
        self.PATIENT= arr[2]
        self.ENCOUNTER= arr[3]
        self.CODE= int(arr[4]) if arr[4].strip() else None
        self.DESCRIPTION = arr[5]
        self.UDI= arr[6]
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(arr=[
                d['START'],
                d['STOP'],
                d['PATIENT'],
                d['ENCOUNTER'],
                d['CODE'],
                d['DESCRIPTION'],
                d['UDI']
        ]
        )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_device_record(obj, ctx):
    if obj is None:
        return None

    return DeviceRecord.from_dict(obj)


def device_record_to_dict(device_record: DeviceRecord, ctx):
    return device_record.__dict__