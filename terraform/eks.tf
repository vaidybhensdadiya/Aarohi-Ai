# =====================================================================
# AMAZON EKS CONTROL PLANE DEFINITION
# =====================================================================
resource "aws_eks_cluster" "main" {
  name     = var.project_name
  role_arn = aws_iam_role.eks_cluster.arn # Hands the required cluster role to EKS
  version  = "1.30"                       # Secure, modern stable Kubernetes release

  vpc_config {
    # Connects the cluster to your isolated security group firewalls
    security_group_ids = [aws_security_group.eks_cluster.id]

    # Places the master control plane interfaces across your private subnets
    subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

    # Best Practice: keeps the cluster API private but accessible over the internet securely
    endpoint_private_access = true
    endpoint_public_access  = true
  }
   public_access_cidrs     = ["172.31.0.0/16"]

  # Ensures IAM roles and policies are fully active on AWS BEFORE the cluster starts provisioning
  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}

