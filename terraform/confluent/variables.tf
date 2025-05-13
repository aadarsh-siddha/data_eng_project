variable "confluent_cloud_api_key" {
  description = "Confluent Cloud API Key (also referred as Cloud API ID)"
  type        = string
  sensitive   = true
}

variable "confluent_cloud_api_secret" {
  description = "Confluent Cloud API Secret"
  type        = string
  sensitive   = true
}

variable "kafka_topics" {
  type    = list(string)
  default = ["patients", "allergies", "careplans", "claims", "claims_transactions", "conditions", "devices", "encounters", "organizations",
    "imaging_studies", "immunizations", "medications", "observations", "payer_transitions", "payers", "procedures", "providers",
    "supplies"]
}

variable "schemas" {
  description = "Map of topic names to schema file paths"
  type        = map(string)
  default = {
    patients             = "schemas/patients.avsc"
    allergies            = "schemas/allergies.avsc"
    medications          = "schemas/medications.avsc"
    observations         = "schemas/observations.avsc"
    procedures           = "schemas/procedures.avsc"
    conditions           = "schemas/conditions.avsc"
    immunizations        = "schemas/immunizations.avsc"
    encounters           = "schemas/encounters.avsc"
    careplans            = "schemas/careplans.avsc"
    devices              = "schemas/devices.avsc"
    imaging_studies      = "schemas/imaging_studies.avsc"
    claims               = "schemas/claims.avsc"
    claims_transactions  = "schemas/claims_transactions.avsc"
    payers               = "schemas/payers.avsc"
    payer_transitions    = "schemas/payer_transitions.avsc"
    providers            = "schemas/providers.avsc"
    supplies             = "schemas/supplies.avsc"
    organizations        = "schemas/organizations.avsc"
  }
}
