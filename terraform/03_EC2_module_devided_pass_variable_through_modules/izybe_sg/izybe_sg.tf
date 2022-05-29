variable "vpc_id" {}

variable "sg_name" {}

resource "aws_security_group" "izybe_sg" {
  name        = var.sg_name
  description = "terraform course sg for ec2 instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "izybe_sg_id" {
  value = aws_security_group.izybe_sg.id
}