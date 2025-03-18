def patient_resource_parser(pat):
    patient_schema = dict()
    patient_schema['last_name'] = pat.name[0].family
    patient_schema['prefix_name'] = pat.name[0].prefix[0]
    patient_schema['first_name'] = pat.name[0].given[0]
    patient_schema['middle_name'] = pat.name[0].given[1] if len(pat.name[0].given) > 1 else None
    patient_schema['ID'] = pat.id 
    for identifier in pat.identifier:
        if identifier.type != None:
            patient_schema[identifier.type.coding[0].code] = identifier.value
    for i,contacts in enumerate(pat.telecom):
        patient_schema[f'phone_{i}'] = contacts.value
    patient_schema['gender'] = getattr(pat, 'gender', None)
    patient_schema['deceased'] = getattr(pat, 'deceased', None)
    patient_schema['deceased_boolean'] = pat.deceasedBoolean
    patient_schema['deceased_timestamp'] = pat.deceasedDateTime
    patient_schema['multiple_birth_boolean'] = pat.multipleBirthBoolean
    patient_schema['multiple_birth_integer'] = pat.multipleBirthInteger
    patient_schema['marital_status'] = (pat.maritalStatus.coding[0].display).lower()
    patient_schema['city'] = pat.address[0].city
    patient_schema['country'] = pat.address[0].country
    patient_schema['postal_code'] = pat.address[0].postalCode
    patient_schema['state'] = pat.address[0].state
    patient_schema['dob'] = pat.birthDate

    return patient_schema


def encounter_resource_parser(encounter):
    encounter_schema = dict()
    encounter_schema['ID'] = encounter.id
    encounter_schema['location'] = encounter.location[0].location.display
    encounter_schema['patient_id'] = encounter.subject.reference
    encounter_schema['snomed_code'] = encounter.type[0].coding[0].code
    encounter_schema['service_provider'] = encounter.serviceProvider.display
    if encounter.reasonCode == None:
        encounter_schema['reason_code'] = None
    else:
        encounter_schema['reason_code'] = encounter.reasonCode[0].coding[0].code
    encounter_schema['end_timestamp'] = encounter.period.end
    encounter_schema['start_timestamp'] = encounter.period.start
    encounter_schema['doctor'] = encounter.participant[0].individual.display

    return encounter_schema


def condition_resource_parser(condition):
    condition_schema = dict()
    if condition.id == None:
        return None
    condition_schema['ID'] = condition.id
    if condition.subject == None:
        return None
    condition_schema['patient_id'] = condition.subject.reference
    condition_schema['clinical_status'] = condition.clinicalStatus.coding[0].code
    condition_schema['verification_status'] = condition.verificationStatus.coding[0].code
    condition_schema['condition_category'] = condition.category[0].coding[0].code
    condition_schema['snomed_code'] = condition.code.coding[0].code
    if condition.bodySite == None:
        condition_schema['body_Site'] = None
    else:
        condition_schema['body_Site'] = condition.bodySite.coding[0].code
    if condition.severity == None:
        condition_schema['severity'] = None
    else:
        condition_schema['severity'] = condition.severity.coding[0].code
    condition_schema['onsetAge'] = getattr(condition, 'onsetAge', None)
    condition_schema['onsetDateTime'] = getattr(condition, 'onsetDateTime', None)
    condition_schema['abatementAge'] = getattr(condition, 'abatementAge', None)
    condition_schema['abatementDateTime'] = getattr(condition, 'abatementDateTime', None)
    condition_schema['recordedDate'] = getattr(condition, 'recordedDate', None)
    condition_schema['stage'] = condition.stage
    condition_schema['evidence'] = condition.evidence

    return condition_schema


def device_resource_parser(device):
    device_schema = dict()
    if device.id == None:
        return None
    device_schema['ID'] = device.id
    device_schema['device_name'] = device.deviceName[0].name
    device_schema['device_type'] = device.deviceName[0].type
    device_schema['lot_number'] = getattr(device, 'lotNumber', None)
    device_schema['definition'] = getattr(device, 'definition', None)
    device_schema['location'] = getattr(device, 'location', None)
    device_schema['distinctIdentifier'] = getattr(device, 'distinctIdentifier', None)
    device_schema['expirationDate'] = getattr(device, 'expirationDate', None)
    device_schema['manufactureDate'] = getattr(device, 'manufactureDate', None)
    device_schema['manufacturer'] = getattr(device, 'manufacturer', None)
    device_schema['serialNumber'] = getattr(device, 'serialNumber', None)
    device_schema['status'] = getattr(device, 'status', None)
    device_schema['udi_id'] = device.udiCarrier[0].carrierHRF
    device_schema['patient_id'] = device.patient.reference

    return device_schema


def diagonistic_report_resource_parser(report):
    diagonistic_report_schema = dict()
    diagonistic_report_schema['ID'] = report.id
    diagonistic_report_schema['patient_id'] = report.subject.reference
    if report.performer != None:
        for i,doctor in enumerate(report.performer):
            diagonistic_report_schema[f'diagnosis_doctor_{i+1}'] = doctor.display
    for i,code_section in enumerate(report.code.coding):
        diagonistic_report_schema[f'diagnosis_loinc_code_{i+1}'] = code_section.code
    
    return diagonistic_report_schema

