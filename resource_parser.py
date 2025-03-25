def codeable_concept_parser(cc):
    if cc == None:
        return None
    code = ""

    for i,codings in enumerate(cc.coding):
        code = code + codings.code
        if i > 0 and i < len(cc.coding):
            code = code + ","
    return code

def n_codeable_concept_parser(codeable_list):
    if codeable_list == None:
        return None
    for i,codeable in enumerate(codeable_list):
        codes = codeable_concept_parser(codeable)
        if i > 0 and i == len(codeable_list) - 1:
            codes += ","

    return codes

def care_team_participant_parser(participants):
    rows = []
    for participant in participants:
        participant_schema = dict()
        participant_schema['ID'] = participant.member.reference
        participant_schema['name'] = participant.member.display
        participant_schema['role_code'] = n_codeable_concept_parser(participant.role)

        rows.append(participant_schema)

    return rows

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

def document_refrence_resource_parser(document_ref):
    document_ref_schema = dict()
    if document_ref.id == None:
        return None
    document_ref_schema['ID'] = document_ref.id
    document_ref_schema['status'] = document_ref.status
    document_ref_schema['patient_id'] = document_ref.subject.reference
    document_ref_schema['date'] = document_ref.date
    document_ref_schema['maintained_by'] = document_ref.custodian.display
    for i, doctor in enumerate(document_ref.author):
        document_ref_schema[f'doctor_name_{i+1}'] = doctor.display
    for i, coding in  enumerate(document_ref.type.coding):
        document_ref_schema[f'document_type_code_{i+1}'] = coding.code ## LOINC Code
    for i, category in enumerate(document_ref.category):
        document_ref_schema[f'category_code_{i+1}'] = ','.join([coding.code for coding in category.coding])
    for i,doc in enumerate(document_ref.content):
        document_ref_schema[f'data_{i+1}'] = doc.attachment.data ## LOINC Code
    for i, encounter in enumerate(document_ref.context.encounter):
        document_ref_schema[f'encounter_id_{i+1}'] = encounter.reference
    
    return document_ref_schema


def claim_resource_parser(claim):
    if claim.id == None:
        return None
    claim_schema = dict()
    claim_schema['ID'] = claim.id
    claim_schema['status'] = getattr(claim, 'status', None)
    claim_schema['claim_type_codes'] = ','.join([codings.code for codings in claim.type.coding])
    claim_schema['claim_use'] = getattr(claim, 'use', None)
    claim_schema['created'] = getattr(claim, 'created', None)
    claim_schema['enterer'] = getattr(claim, 'enterer', None)
    claim_schema['insurer'] = getattr(claim, 'insurer', None)
    claim_schema['provider'] = getattr(claim, 'provider', None)
    claim_schema['created'] = getattr(claim, 'created', None)
    claim_schema['prescription'] = getattr(claim, 'prescription', None)
    claim_schema['related'] = getattr(claim, 'related', None)
    claim_schema['referral'] = getattr(claim, 'referral', None)
    claim_schema['payee'] = getattr(claim, 'payee', None)
    claim_schema['procedure'] = getattr(claim, 'procedure', None)
    claim_schema['originalPrescription'] = getattr(claim, 'originalPrescription', None)
    claim_schema['careTeam'] = getattr(claim, 'careTeam', None)
    claim_schema['careTeam'] = getattr(claim, 'careTeam', None)
    claim_schema['accident'] = getattr(claim, 'accident', None)
    claim_schema['patient_id'] = claim.patient.reference
    claim_schema['billable_start'] = claim.billablePeriod.start
    claim_schema['billable_end'] = claim.billablePeriod.end
    claim_schema['claim_priority_code'] = claim.priority.coding[0].code
    if claim.facility != None:
        claim_schema['facility'] = claim.facility.display
    else:
        claim_schema['facility'] = None
    if claim.diagnosis != None:
        claim_schema['diagnosis_refrence_id'] = claim.diagnosis[0].diagnosisReference.reference
    else:
        claim_schema['diagnosis_refrence_id'] = None
    for i, insurance in enumerate(claim.insurance):
        claim_schema[f'insurance_{i+1}'] = insurance.coverage.display
    claim_schema['claim_amount'] = claim.total.value

    return claim_schema

def explaination_ob_resource_parser(explain_ob):
    if explain_ob.id == None:
        return None
    explain_ob_schema = dict()
    explain_ob_schema['ID'] = explain_ob.id
    explain_ob_schema['status'] = getattr(explain_ob, 'status', None)
    explain_ob_schema['type_code'] = codeable_concept_parser(explain_ob.type)
    explain_ob_schema['use'] = getattr(explain_ob, 'use', None)
    explain_ob_schema['patient_id'] = getattr(getattr(explain_ob, 'patient', None), 'refrence', None)
    explain_ob_schema['billable_start_date'] = getattr(getattr(explain_ob, 'billablePeriod', None), 'start', None)
    explain_ob_schema['billable_end_date'] = getattr(getattr(explain_ob, 'billablePeriod', None), 'start', None)
    explain_ob_schema['created'] = getattr(explain_ob,'created', None)
    explain_ob_schema['insurer'] = getattr(getattr(explain_ob, 'insurer', None), 'display', None)
    explain_ob_schema['provider'] = getattr(getattr(explain_ob, 'provider', None), 'reference', None)
    explain_ob_schema['outcome'] = getattr(explain_ob, 'outcome', None)
    explain_ob_schema['claim_id'] = getattr(getattr(explain_ob, 'claim', None), 'reference', None)
    explain_ob_schema['procedure'] = explain_ob.procedure
    for careteam in explain_ob.careTeam:
        explain_ob_schema[f'careteam_{careteam.sequence}_reference_id'] = careteam.provider.reference
    for diagnosis in explain_ob.diagnosis:
        explain_ob_schema[f'diagnosis_{diagnosis.sequence}_reference_id'] = diagnosis.diagnosisReference.reference
    for i,insurance in enumerate(explain_ob.insurance):
        explain_ob_schema[f'insurance_{i+1}'] = insurance.coverage.display


    return explain_ob_schema


def observation_resource_parser(obs):
    if obs.id == None:
        return None
    observation_schema = dict()
    observation_schema['ID'] = obs.id
    observation_schema['based_on'] = getattr(obs,'basedOn', None)
    observation_schema['part_of'] = getattr(obs,'partOf', None)
    observation_schema['status'] = getattr(obs,'status', None)
    observation_schema['category_type'] = n_codeable_concept_parser(obs.category)
    observation_schema['loinc_code'] = codeable_concept_parser(obs.code)
    observation_schema['patient_id'] = getattr(getattr(obs,'subject',None),'reference',None)
    observation_schema['focus'] = getattr(obs, 'focus', None)
    observation_schema['encounter_id'] = getattr(getattr(obs,'encounter',None),'reference',None)
    observation_schema['effective_datetime'] = getattr(obs, 'effectiveDateTime', None)
    observation_schema['effective_period'] = getattr(obs, 'effectivePeriod', None)
    observation_schema['effective_timing'] = getattr(obs, 'effectiveTiming', None)
    observation_schema['issued'] = getattr(obs, 'issued', None)
    observation_schema['performer'] = getattr(obs, 'performer', None)
    observation_schema['value_boolean'] = getattr(obs, 'valueBoolean', None)
    observation_schema['value_codeable_concept'] = getattr(obs, 'valueCodeableConcept', None)
    observation_schema['value_datetime'] = getattr(obs, 'valueDateTime', None)
    observation_schema['value_integer'] = getattr(obs, 'valueInteger', None)
    observation_schema['value_unit'] = getattr(getattr(obs,'valueQuantity',None),'unit',None)
    observation_schema['value'] = getattr(getattr(obs,'valueQuantity',None),'value',None)
    observation_schema['value_tring'] = getattr(obs, 'valueString', None)
    observation_schema['data_absent_reason'] = getattr(obs, 'dataAbsentReason', None)
    observation_schema['interpretation'] = getattr(obs, 'interpretation', None)
    observation_schema['note'] = getattr(obs, 'note', None)
    observation_schema['bodysite'] = getattr(obs, 'bodySite', None)
    observation_schema['method'] = getattr(obs, 'method', None)
    observation_schema['specimen'] = getattr(obs, 'specimen', None)
    observation_schema['device'] = getattr(obs, 'device', None)
    observation_schema['reference_range'] = getattr(obs, 'referenceRange', None)
    observation_schema['has_member'] = getattr(obs, 'hasMember', None)
    observation_schema['derived_from'] = getattr(obs, 'derivedFrom', None)
    observation_schema['component'] = getattr(obs, 'component', None)

    return observation_schema    


def care_team_resource_parser(care_team):
    if care_team.id == None:
        return None
    care_team_schema = dict()
    care_team_schema['id'] = care_team.id
    care_team_schema['status'] = getattr(care_team,'status',None)
    care_team_schema['category_code'] = n_codeable_concept_parser(care_team.category)
    care_team_schema['name'] = getattr(care_team,'name',None)
    care_team_schema['patient_id'] = getattr(getattr(care_team,'subject',None),'reference',None)
    care_team_schema['encounter_id'] = getattr(getattr(care_team,'encounter',None),'reference',None)
    care_team_schema['period_start'] = getattr(getattr(care_team,'period',None),'start',None)
    care_team_schema['period_end'] = getattr(getattr(care_team,'period',None),'end',None)
    care_team_schema['participants'] = care_team_participant_parser(care_team.participant)
    care_team_schema['reasonCode'] = n_codeable_concept_parser(getattr(care_team,'reasonCode',None))
    care_team_schema['reasonReference'] = getattr(care_team,'reasonReference',None)
    care_team_schema['note'] = getattr(care_team,'note',None)
    care_team_schema['telecom'] = getattr(care_team,'telecom',None)
    for i,org in enumerate(care_team.managingOrganization):
        care_team_schema[f'managing_org_{i+1}_name'] = org.display     
        care_team_schema[f'managing_org_{i+1}_id'] = org.reference

    return care_team_schema

def care_plan_activity_parser(activities):
    rows = []
    for activity in activities:
        activity_schema = dict()
        activity_schema['outcome_code'] = n_codeable_concept_parser(activity.outcomeCodeableConcept)
        activity_schema['outcomeReference'] = getattr(activity,'outcomeReference',None)
        activity_schema['progress'] = getattr(activity,'progress',None)
        activity_schema['reference'] = getattr(activity,'reference',None)
        activity_schema['note'] = getattr(activity,'note',None)
        activity_schema['instantiates_canonical'] = getattr(getattr(activity,'detail',None),'instantiatesCanonical',None)
        activity_schema['instantiates_uri'] = getattr(getattr(activity,'detail',None),'instantiatesUri',None)
        activity_schema['code'] = codeable_concept_parser(getattr(getattr(activity,'detail',None),'code',None))
        activity_schema['reason_code'] = n_codeable_concept_parser(getattr(getattr(activity,'detail',None),'reasonCode',None))
        activity_schema['reason_reference'] = getattr(getattr(activity,'detail',None),'reasonReference',None)
        activity_schema['goal'] = getattr(getattr(activity,'detail',None),'goal',None)
        activity_schema['status'] = getattr(getattr(activity,'detail',None),'status',None)
        activity_schema['status_reason'] = getattr(getattr(activity,'detail',None),'statusReason',None)
        activity_schema['do_not_perform'] = getattr(getattr(activity,'detail',None),'doNotPerform',None)
        activity_schema['location'] = getattr(getattr(activity,'detail',None),'location',None).display
        activity_schema['daily_amount'] = getattr(getattr(activity,'detail',None),'dailyAmount',None)
        activity_schema['product'] = getattr(getattr(activity,'detail',None),'product',None)
        rows.append(activity_schema)

    return rows


def care_plan_resource_parser(care_plan):
    care_plan_schema = dict()
    care_plan_schema['id'] = getattr(care_plan,'id',None)
    care_plan_schema['instantiates_canonical'] = getattr(care_plan,'instantiatesCanonical',None)
    care_plan_schema['instantiatesUri'] = getattr(care_plan,'instantiatesUri',None)
    care_plan_schema['basedOn'] = getattr(care_plan,'basedOn',None)
    care_plan_schema['partOf'] = getattr(care_plan,'partOf',None)
    care_plan_schema['status'] = getattr(care_plan,'status',None)
    care_plan_schema['intent'] = getattr(care_plan,'intent',None)
    care_plan_schema['category_code'] = n_codeable_concept_parser(getattr(care_plan,'category',None))
    care_plan_schema['title'] = getattr(care_plan,'title',None)
    care_plan_schema['subject'] = getattr(getattr(care_plan,'subject',None),'reference',None)
    care_plan_schema['encounter'] = getattr(getattr(care_plan,'encounter',None),'reference',None)
    care_plan_schema['period_start'] = getattr(getattr(care_plan,'period',None),'start',None)
    care_plan_schema['period_end'] = getattr(getattr(care_plan,'period',None),'end',None)
    care_plan_schema['created'] = getattr(care_plan,'created',None)
    care_plan_schema['author'] = getattr(care_plan,'author',None)
    care_plan_schema['contributor'] = getattr(care_plan,'contributor',None)
    care_plan_schema['created'] = getattr(care_plan,'created',None)
    for i,care_team in enumerate(getattr(care_plan,'careTeam',None)):
        care_plan_schema[f'care_team_{i+1}_id'] = care_team.reference
    care_plan_schema['addresses'] = getattr(care_plan,'addresses',None)
    care_plan_schema['created'] = getattr(care_plan,'created',None)
    care_plan_schema['goal'] = getattr(care_plan,'goal',None)
    care_plan_schema['activities'] = care_plan_activity_parser(care_plan.activity)

    return care_plan_schema


def allergy_intolerance_resource_parser(allergy_intolerance):
    allergy_intolerance_schema = dict()
    allergy_intolerance_schema['id'] = getattr(allergy_intolerance,'id',None)
    allergy_intolerance_schema['clinical_status'] = codeable_concept_parser(getattr(allergy_intolerance,'clinicalStatus',None))
    allergy_intolerance_schema['verification_status'] = codeable_concept_parser(getattr(allergy_intolerance,'verificationStatus',None))
    allergy_intolerance_schema['type'] = getattr(allergy_intolerance,'type',None)
    allergy_intolerance_schema['category'] = getattr(allergy_intolerance,'category',None)
    allergy_intolerance_schema['criticality'] = getattr(allergy_intolerance,'criticality',None)
    allergy_intolerance_schema['patient_id'] = getattr(getattr(allergy_intolerance,'patient',None),'reference',None)
    allergy_intolerance_schema['encounter_id'] = getattr(getattr(allergy_intolerance,'encounter',None),'reference',None)
    allergy_intolerance_schema['onset_age'] = getattr(allergy_intolerance,'onsetAge',None)
    allergy_intolerance_schema['recorded_date'] = getattr(allergy_intolerance,'recordedDate',None)
    allergy_intolerance_schema['onset_period'] = getattr(allergy_intolerance,'onsetPeriod',None)
    allergy_intolerance_schema['onset_range'] = getattr(allergy_intolerance,'onsetRange',None)    
    allergy_intolerance_schema['recorder'] = getattr(allergy_intolerance,'recorder',None)
    allergy_intolerance_schema['asserter'] = getattr(allergy_intolerance,'asserter',None)
    allergy_intolerance_schema['note'] = getattr(allergy_intolerance,'note',None)
    allergy_intolerance_schema['last_occurrence'] = getattr(allergy_intolerance,'lastOccurrence',None)
    allergy_intolerance_schema['reaction_substance'] = codeable_concept_parser(getattr(getattr(allergy_intolerance,'reaction',None),'substance',None))
    allergy_intolerance_schema['reaction_manifestation'] = n_codeable_concept_parser(getattr(getattr(allergy_intolerance,'reaction',None),'manifestation',None))
    allergy_intolerance_schema['reaction_onset'] = getattr(getattr(allergy_intolerance,'reaction',None),'onset',None)
    allergy_intolerance_schema['reaction_severity'] = getattr(getattr(allergy_intolerance,'reaction',None),'severity',None)
    allergy_intolerance_schema['reaction_exposure_route'] = codeable_concept_parser(getattr(getattr(allergy_intolerance,'reaction',None),'exposureRoute',None))

    return allergy_intolerance_schema


def dosage_instruction_parser(dosage_instructions):
    return None

def medication_request_resource_parser(medication_request):
    medication_request_schema = dict()
    medication_request_schema['id'] = getattr(medication_request,'id',None)
    medication_request_schema['status'] = getattr(medication_request,'status',None)
    medication_request_schema['status_reason'] = codeable_concept_parser(getattr(medication_request,'statusReason',None))
    medication_request_schema['intent'] = getattr(medication_request,'intent',None)
    medication_request_schema['category'] = n_codeable_concept_parser(getattr(medication_request,'category',None))
    medication_request_schema['priority'] = getattr(medication_request,'priority',None)
    medication_request_schema['do_not_perform'] = getattr(medication_request,'doNotPerform',None)
    medication_request_schema['reported_boolean'] = getattr(medication_request,'reportedBoolean',None)
    medication_request_schema['reported_reference_id'] = getattr(getattr(medication_request,'reportedReference',None),'reference',None)
    medication_request_schema['subject'] = getattr(getattr(medication_request,'subject',None),'reference',None)
    medication_request_schema['encounter'] = getattr(getattr(medication_request,'encounter',None),'reference',None)
    medication_request_schema['authored_on'] = getattr(medication_request,'authoredOn',None)
    medication_request_schema['requester'] = getattr(getattr(medication_request,'requester',None),'reference',None)
    medication_request_schema['performer'] = getattr(medication_request,'performer',None)
    medication_request_schema['performer_type'] = getattr(medication_request,'performerType',None)
    medication_request_schema['recorder'] = getattr(medication_request,'recorder',None)
    medication_request_schema['reason_code'] = n_codeable_concept_parser(getattr(medication_request,'reasonCode',None))
    medication_request_schema['instantiates_canonical'] = getattr(medication_request,'instantiatesCanonical',None)
    medication_request_schema['based_on'] = getattr(medication_request,'basedOn',None)
    medication_request_schema['group_identifier'] = getattr(medication_request,'groupIdentifier',None)
    medication_request_schema['course_of_therapy_type'] = getattr(medication_request,'courseOfTherapyType',None)
    medication_request_schema['insurance'] = getattr(medication_request,'insurance',None)
    medication_request_schema['note'] = getattr(medication_request,'note',None)
    medication_request_schema['dosage_instruction'] = dosage_instruction_parser(getattr(medication_request,'dosageInstruction',None))
    medication_request_schema['dispense_request'] = getattr(medication_request,'dispenseRequest',None)
    medication_request_schema['dispense_request'] = getattr(medication_request,'dispenseRequest',None)

    return medication_request_schema
    

def procedure_resource_parser(procedure):
    procedure_schema = dict()
    procedure_schema['id'] = getattr(procedure,'id',None)
    procedure_schema['instantiates_canonical'] = getattr(procedure,'instantiatesCanonical',None)
    procedure_schema['based_on'] = getattr(procedure,'basedOn',None)
    procedure_schema['part_of'] = getattr(procedure,'partOf',None)
    procedure_schema['status'] = getattr(procedure,'status',None)
    procedure_schema['status_reason'] = codeable_concept_parser(getattr(procedure,'statusReason',None))
    procedure_schema['code'] = codeable_concept_parser(getattr(procedure,'code',None))
    procedure_schema['category'] = codeable_concept_parser(getattr(procedure,'category',None))
    procedure_schema['subject'] = getattr(getattr(procedure,'subject',None),'reference',None)
    procedure_schema['encounter'] = getattr(getattr(procedure,'encounter',None),'reference',None)
    procedure_schema['performed_age'] = getattr(procedure,'performedAge',None)
    procedure_schema['performed_datetime'] = getattr(procedure,'performedDateTime',None)
    procedure_schema['performed_period_start'] = getattr(getattr(procedure,'performedPeriod',None),'start',None)
    procedure_schema['performed_period_end'] = getattr(getattr(procedure,'performedPeriod',None),'end',None)
    procedure_schema['performed_string'] = getattr(procedure,'performedString',None)
    procedure_schema['recorder'] = getattr(procedure,'recorder',None)
    procedure_schema['asserter'] = getattr(procedure,'asserter',None)
    procedure_schema['performer'] = getattr(procedure,'performer',None)
    procedure_schema['location'] = getattr(getattr(procedure,'location',None),'reference',None)
    procedure_schema['reason_code'] = getattr(procedure,'reasonCode',None)
    procedure_schema['body_site'] = getattr(procedure,'bodySite',None)
    procedure_schema['outcome'] = getattr(procedure,'outcome',None)
    if getattr(procedure,'reasonReference',None):
        procedure_schema['reason_reference'] = procedure.reasonReference[0].reference
    else:
        procedure_schema['reason_reference'] = None
    return procedure_schema



