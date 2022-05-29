variable "ami_id" {}


variable "key_pair_label" {}

variable "instance_type" {}

variable "tag_name" {}

variable "sg_id" {}

variable "subnet_id" {}

resource "aws_instance" "dev_ec2_instance" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_pair_label
  vpc_security_group_ids = [var.sg_id]
  subnet_id = var.subnet_id

  tags = {
    Name = var.tag_name
  }
}

