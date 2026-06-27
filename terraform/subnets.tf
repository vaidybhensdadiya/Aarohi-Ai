# --- Public Subnets (For Ingress Load Balancers) ---
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
   # nosemgrep: terraform.aws.security.aws-subnet-has-public-ip-address.aws-subnet-has-public-ip-address
  map_public_ip_on_launch = true

  tags = {
    Name                                        = "${var.project_name}-public-1"
    "kubernetes.io/cluster/${var.project_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1" # Tells AWS ALB Controller to use this for public LBs
  }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.aws_region}c"
   # nosemgrep: terraform.aws.security.aws-subnet-has-public-ip-address.aws-subnet-has-public-ip-address
  
  map_public_ip_on_launch = true

  tags = {
    Name                                        = "${var.project_name}-public-2"
    "kubernetes.io/cluster/${var.project_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }
}

# --- Private Subnets (For EKS Worker Nodes & Database) ---
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name                                        = "${var.project_name}-private-1"
    "kubernetes.io/cluster/${var.project_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1" # Tells AWS ALB Controller to use this for internal LBs
  }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.12.0/24"
  availability_zone = "${var.aws_region}c"

  tags = {
    Name                                        = "${var.project_name}-private-2"
    "kubernetes.io/cluster/${var.project_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

