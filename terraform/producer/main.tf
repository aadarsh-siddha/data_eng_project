terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.96.0"
    }
  }
}


resource "aws_ecr_repository" "kafka_producer_repo" {
  name = "kafka-producer"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name        = "kafka-producer-repo"
    Environment = "staging"
  }
}
