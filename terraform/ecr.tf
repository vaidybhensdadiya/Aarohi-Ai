resource "aws_ecr_repository" "web_app" {
  name                 = "${var.project_name}-web-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true # Native AWS security scan on top of our pipeline scans
  }

  tags = {
    Name = "${var.project_name}-ecr"
  }
}

# Output the repository URL so our pipeline can find it
output "ecr_repository_url" {
  value       = aws_ecr_repository.web_app.repository_url
  description = "The target private AWS registry URL destination endpoint"
}

