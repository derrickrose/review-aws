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

data "aws_subnet" "subnet_public" {
  vpc_id = data.aws_vpcs.izybe_vpcs.ids[0]
  tags   = {
    Name = "IzybeVpcDev-subnet-public-a"
  }
}

locals {
  dev_izybe_public_key     = file("id_rsa.pub")
  dev_izybe_ec2_ami_id     = "ami-0a21d1c76ac56fee7"
  dev_izybe_vpc_id         = data.aws_vpcs.izybe_vpcs.ids[0] #vpc-9c82b8f5
  dev_izybe_key_pair_label = "dev-izybe-ec2-key-pair"
  dev_izybe_tag_name       = "dev-izybe-ec2"
  dev_izybe_sg_name        = "dev-izybe-sg"
  dev_izybe_instance_type  = "t2.micro"
  dev_izybe_subnet_id      = data.aws_subnet.subnet_public.id

}

resource "aws_key_pair" "izybe_key_pair" {
  public_key = local.dev_izybe_public_key
  key_name   = local.dev_izybe_key_pair_label
  tags       = {
    name = local.dev_izybe_key_pair_label
  }

}

module "dev_izybe_sg" {
  source  = "./izybe_sg"
  vpc_id  = local.dev_izybe_vpc_id
  sg_name = local.dev_izybe_sg_name
}


#module "dev_izybe_ec2" {
#  depends_on     = [aws_key_pair.izybe_key_pair]
#  source         = "./izybe_ec2"
#  ami_id         = local.dev_izybe_ec2_ami_id
#  key_pair_label = local.dev_izybe_key_pair_label
#  tag_name       = local.dev_izybe_tag_name
#  sg_id          = module.dev_izybe_sg.izybe_sg_id
#  instance_type  = local.dev_izybe_instance_type
#  subnet_id      = local.dev_izybe_subnet_id
#}



