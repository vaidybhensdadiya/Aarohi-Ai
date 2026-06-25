# =====================================================================
# AMAZON EKS MANAGED NODE GROUP DEFINITION
# =====================================================================
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-node-group"
  node_role_arn   = aws_iam_role.eks_nodes.arn                         # Hands permissions to your instances
  subnet_ids      = [aws_subnet.private_1.id, aws_subnet.private_2.id] # Places worker nodes safely in private subnets

  # Cost Optimization Settings
  capacity_type  = "SPOT"        # 💰 Uses AWS Spot Instances to drastically cut infrastructure costs
  instance_types = ["t2.medium"] # Perfect balance of CPU & RAM for running lightweight Flask + ML containers

  scaling_config {
    desired_size = 2 # Matches your required 2-pod architecture footprint
    min_size     = 1
    max_size     = 2 # Allows room for your HPA to autoscale up during traffic bursts
  }

  update_config {
    max_unavailable = 1 # Zero-downtime rolling upgrades constraint
  }

  # Ensures underlying node network frameworks are up before EC2 instances boot
  depends_on = [
    aws_iam_role_policy_attachment.amazon_eks_worker_node_policy,
    aws_iam_role_policy_attachment.amazon_eks_cni_policy,
    aws_iam_role_policy_attachment.amazon_ecr_read_only,
  ]
}

