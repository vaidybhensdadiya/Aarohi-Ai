output "cluster_name" {
  value       = aws_eks_cluster.main.name
  description = "The unique identity label of the EKS Cluster"
}

output "cluster_endpoint" {
  value       = aws_eks_cluster.main.endpoint
  description = "The secure HTTP link to pass commands into your Kubernetes API master"
}

output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The physical network ID container blueprint"
}

