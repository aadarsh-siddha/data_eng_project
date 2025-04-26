terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "2.25.0"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.96.0"
    }
  }
}

provider "confluent" {
  cloud_api_key    = var.confluent_cloud_api_key
  cloud_api_secret = var.confluent_cloud_api_secret
}

resource "confluent_environment" "staging" {
  display_name = "fhir_kafka_stream"

  stream_governance {
    package = "ESSENTIALS"
  }
}

# Update the config to use a cloud provider and region of your choice.
# https://registry.terraform.io/providers/confluentinc/confluent/latest/docs/resources/confluent_kafka_cluster
resource "confluent_kafka_cluster" "standard" {
  display_name = "inventory"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = "us-east-1"
  standard {}
  environment {
    id = confluent_environment.staging.id
  }
}

// 'app-manager' service account is required in this configuration to create 'patients' topic and assign roles
// to 'app-producer' and 'app-consumer' service accounts.
resource "confluent_service_account" "app-manager" {
  display_name = "app-manager"
  description  = "Service account to manage 'inventory' Kafka cluster"
}

resource "confluent_role_binding" "app-manager-kafka-cluster-admin" {
  principal   = "User:${confluent_service_account.app-manager.id}"
  role_name   = "CloudClusterAdmin"
  crn_pattern = confluent_kafka_cluster.standard.rbac_crn
}

resource "confluent_api_key" "app-manager-kafka-api-key" {
  display_name = "app-manager-kafka-api-key"
  description  = "Kafka API Key that is owned by 'app-manager' service account"
  owner {
    id          = confluent_service_account.app-manager.id
    api_version = confluent_service_account.app-manager.api_version
    kind        = confluent_service_account.app-manager.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.standard.id
    api_version = confluent_kafka_cluster.standard.api_version
    kind        = confluent_kafka_cluster.standard.kind

    environment {
      id = confluent_environment.staging.id
    }
  }

  # The goal is to ensure that confluent_role_binding.app-manager-kafka-cluster-admin is created before
  # confluent_api_key.app-manager-kafka-api-key is used to create instances of
  # confluent_kafka_topic, confluent_kafka_acl resources.

  # 'depends_on' meta-argument is specified in confluent_api_key.app-manager-kafka-api-key to avoid having
  # multiple copies of this definition in the configuration which would happen if we specify it in
  # confluent_kafka_topic, confluent_kafka_acl resources instead.
  depends_on = [
    confluent_role_binding.app-manager-kafka-cluster-admin
  ]
}

resource "confluent_kafka_topic" "topics" {
  for_each = toset(var.kafka_topics)

  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = each.key
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  
  partitions_count = 2

  config = {
    "retention.ms" = 86400000   # 1 day 
  }

  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_service_account" "app-consumer" {
  display_name = "app-consumer"
  description  = "Service account to consume from 'patients' topic of 'inventory' Kafka cluster"
}

resource "confluent_api_key" "app-consumer-kafka-api-key" {
  display_name = "app-consumer-kafka-api-key"
  description  = "Kafka API Key that is owned by 'app-consumer' service account"
  owner {
    id          = confluent_service_account.app-consumer.id
    api_version = confluent_service_account.app-consumer.api_version
    kind        = confluent_service_account.app-consumer.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.standard.id
    api_version = confluent_kafka_cluster.standard.api_version
    kind        = confluent_kafka_cluster.standard.kind

    environment {
      id = confluent_environment.staging.id
    }
  }
}

resource "confluent_role_binding" "app-producer-developer-write" {
  for_each   = toset(var.kafka_topics)
  principal   = "User:${confluent_service_account.app-producer.id}"
  role_name   = "DeveloperWrite"
  crn_pattern = "${confluent_kafka_cluster.standard.rbac_crn}/kafka=${confluent_kafka_cluster.standard.id}/topic=${each.key}"
}

resource "confluent_service_account" "app-producer" {
  display_name = "app-producer"
  description  = "Service account to produce to 'patients' topic of 'inventory' Kafka cluster"
}

resource "confluent_api_key" "app-producer-kafka-api-key" {
  display_name = "app-producer-kafka-api-key"
  description  = "Kafka API Key that is owned by 'app-producer' service account"
  owner {
    id          = confluent_service_account.app-producer.id
    api_version = confluent_service_account.app-producer.api_version
    kind        = confluent_service_account.app-producer.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.standard.id
    api_version = confluent_kafka_cluster.standard.api_version
    kind        = confluent_kafka_cluster.standard.kind

    environment {
      id = confluent_environment.staging.id
    }
  }
}

// Note that in order to consume from a topic, the principal of the consumer ('app-consumer' service account)
// needs to be authorized to perform 'READ' operation on both Topic and Group resources:
resource "confluent_role_binding" "app-consumer-developer-read-from-topic" {
  for_each   = toset(var.kafka_topics)
  principal   = "User:${confluent_service_account.app-consumer.id}"
  role_name   = "DeveloperRead"
  crn_pattern = "${confluent_kafka_cluster.standard.rbac_crn}/kafka=${confluent_kafka_cluster.standard.id}/topic=${each.key}"
}

resource "confluent_role_binding" "app-consumer-developer-read-from-group" {
  principal = "User:${confluent_service_account.app-consumer.id}"
  role_name = "DeveloperRead"
  // The existing value of crn_pattern's suffix (group=confluent_cli_consumer_*) are set up to match Confluent CLI's default consumer group ID ("confluent_cli_consumer_<uuid>").
  // https://docs.confluent.io/confluent-cli/current/command-reference/kafka/topic/confluent_kafka_topic_consume.html
  // Update it to match your target consumer group ID.
  crn_pattern = "${confluent_kafka_cluster.standard.rbac_crn}/kafka=${confluent_kafka_cluster.standard.id}/group=confluent_cli_consumer_*"
}



# Schema Registry Setup

data "confluent_schema_registry_cluster" "essentials" {
  environment {
    id = confluent_environment.staging.id
  }

  depends_on = [
    confluent_kafka_cluster.standard
  ]
}

resource "confluent_api_key" "schema_registry_api_key" {
  display_name = "schema-registry-api-key"
  description  = "API Key for Schema Registry access"

  owner {
    id          = confluent_service_account.app-manager.id
    api_version = confluent_service_account.app-manager.api_version
    kind        = confluent_service_account.app-manager.kind
  }

  managed_resource {
    id          = data.confluent_schema_registry_cluster.essentials.id
    api_version = data.confluent_schema_registry_cluster.essentials.api_version
    kind        = data.confluent_schema_registry_cluster.essentials.kind

    environment {
      id = confluent_environment.staging.id
    }
  }

  depends_on = [data.confluent_schema_registry_cluster.essentials]
}

resource "aws_secretsmanager_secret" "producer_kafka_config" {
  name = "confluent-producer-kafka-config"
}

resource "aws_secretsmanager_secret_version" "producer_kafka_config_version" {
  secret_id = aws_secretsmanager_secret.producer_kafka_config.id

  secret_string = jsonencode({
    bootstrap_server            = confluent_kafka_cluster.standard.bootstrap_endpoint
    sasl_protocol               = "SASL_SSL"
    sasl_mechanism              = "PLAIN"
    kafka_api_key               = confluent_api_key.app-producer-kafka-api-key.id
    kafka_api_secret            = confluent_api_key.app-producer-kafka-api-key.secret
    schema_registry_endpoint    = data.confluent_schema_registry_cluster.essentials.rest_endpoint
    schema_registry_api_key     = confluent_api_key.schema_registry_api_key.id
    schema_registry_api_secret  = confluent_api_key.schema_registry_api_key.secret
    schema_registry_environment = confluent_environment.staging.id
  })

  depends_on = [
    confluent_api_key.app-producer-kafka-api-key,
    confluent_api_key.schema_registry_api_key
  ]
}
