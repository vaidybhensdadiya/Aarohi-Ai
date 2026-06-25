
# =====================================================================
# 1. APPLICATION LOAD BALANCER (ALB) SECURITY GROUP
# =====================================================================
# This is your front-line public firewall. It allows users from the internet
# to reach your NGINX Ingress controller over standard web ports.
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Public-facing firewall for the Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP traffic from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS traffic from anywhere (for future SSL activation)
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic (ALB routing requests to worker nodes)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}

# =====================================================================
# 2. EKS CONTROL PLANE SECURITY GROUP
# =====================================================================
# Protects the Kubernetes Master API engine. It only opens up access to 
# worker nodes that need to receive management instructions.
resource "aws_security_group" "eks_cluster" {
  name        = "${var.project_name}-cluster-sg"
  description = "Protects the EKS control plane API endpoint"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-cluster-sg"
  }
}

# =====================================================================
# 3. EKS WORKER NODES SECURITY GROUP
# =====================================================================
# Governs the EC2 instances where your Flask app and MySQL pods run.
resource "aws_security_group" "eks_nodes" {
  name        = "${var.project_name}-node-sg"
  description = "Governs firewall boundaries for EKS worker nodes"
  vpc_id      = aws_vpc.main.id

  # Allow nodes to talk to each other freely on all ports
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }

  # Allow the Control Plane Master API to send instructions to pods
  ingress {
    from_port       = 10250
    to_port         = 10250
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster.id]
  }

  # Allow public ALB to forward traffic to the NGINX Ingress on NodePort ranges
  ingress {
    from_port       = 30000
    to_port         = 32767
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # Allow nodes to reach out to the internet (via NAT) to pull images/weights
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name                                        = "${var.project_name}-node-sg"
    "kubernetes.io/cluster/${var.project_name}" = "owned"
  }
}
resource "aws_security_group_rule" "cluster_inbound_nodes" {
  description              = "Allow worker nodes to communicate with the cluster API server"
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.eks_cluster.id
  source_security_group_id = aws_security_group.eks_nodes.id
}

