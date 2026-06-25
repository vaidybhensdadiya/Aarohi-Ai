# NAT Gateway requires a Static Public IP (Elastic IP)
resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-nat-eip"
  }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_1.id # Lives in a public subnet to touch the internet

  tags = {
    Name = "${var.project_name}-nat-gw"
  }

  depends_on = [aws_internet_gateway.main] # Best practice: waits for IGW to exist first
}

