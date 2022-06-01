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
  subnet_id              = var.subnet_id

  timeouts {
    create = "2h"
    delete = "2h"
  }

  tags = {
    Name = var.tag_name
  }






  #  connection {
  #    type        = "ssh"
  #    user        = "ec2-user"
  #    password    = ""
  #    private_key = file(var.keyPath)
  #    host        = self.public_ip
  #  }
}


resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.dev_ec2_instance.id
  allocation_id = aws_eip.eip.id
}

resource "aws_eip" "eip" {
  vpc = true
}
