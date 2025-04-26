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
  default = ["patients", "allergies", "careplans", "claims", "claims_transactions", "conditions", "devices", "encounters", 
    "imaging_studies", "immunizations", "medications", "observations", "payer_transitions", "payers", "procedures", "providers",
    "supplies"]
}
