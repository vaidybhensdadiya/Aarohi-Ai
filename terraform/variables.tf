variable "aws_region" {
  type        = string
  description = "The target AWS geographic deployment region"
}

variable "project_name" {
  type        = string
  description = "The name mapping associated with this infrastructure stack"
}

variable "vpc_cidr" {
  type        = string
  description = "The primary IPv4 CIDR allocation block for the custom VPC"
}

