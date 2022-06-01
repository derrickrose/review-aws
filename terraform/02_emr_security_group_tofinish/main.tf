provider "aws" {
  region  = "eu-west-3"
  profile = "dev-izybe"
}

data "aws_vpcs" "izybe_vpcs" {
  filter {
    name   = "tag:Name"
    values = ["IzybeVpcDev"]
  }
}


locals {
  izybe_sg_emr_master_name = "dev-izybe-sg-emr-master"
  izybe_sg_emr_slave_name  = "dev-izybe-sg-emr-slave"
}

resource "aws_security_group" "izybe_sg_emr_master" {
  name        = local.izybe_sg_emr_master_name
  description = "terraform course sg for ec2 instance"
  vpc_id      = data.aws_vpcs.izybe_vpcs.ids[0]

  ingress {
    description = "all-icmp-ipv4"
    from_port   = 0
    protocol    = "all"
    to_port     = 65535
  }

  ingress {
    description = "all-tcp"
    from_port   = 0
    protocol    = "tcp"
    to_port     = 65535
  }

  ingress {
    description = "all-udp"
    from_port   = 0
    protocol    = "udp"
    to_port     = 65535
  }


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

resource "aws_security_group" "izybe_sg_emr_slave" {
  name        = local.izybe_sg_emr_slave_name
  description = "terraform course sg for ec2 instance"
  vpc_id      = data.aws_vpcs.izybe_vpcs.ids[0]


  ingress {
    description = "all-icmp-ipv4"
    from_port   = 0
    protocol    = "all"
    to_port     = 65535
  }

  ingress {
    description = "all-tcp"
    from_port   = 0
    protocol    = "tcp"
    to_port     = 65535
  }

  ingress {
    description = "all-udp"
    from_port   = 0
    protocol    = "udp"
    to_port     = 65535
  }
}