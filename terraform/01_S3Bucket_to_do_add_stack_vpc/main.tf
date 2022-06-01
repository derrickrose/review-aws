provider "aws" {
  region  = "eu-west-1"
  profile = "dev-izybe"
}


resource "aws_s3_bucket" "dev_izybe_bucket" {
  bucket = "dev-izybe-bucket"
  #  acl    = "private"
  tags   = {
    Environment = "dev"
  }
}

resource "aws_s3_bucket_acl" "dev_izybe_bucket_acl" {
  bucket     = aws_s3_bucket.dev_izybe_bucket.id
  depends_on = [aws_s3_bucket.dev_izybe_bucket]
  acl = "private"

}


resource "aws_s3_object" "my_first_object" {
  bucket     = aws_s3_bucket.dev_izybe_bucket.id
  depends_on = [aws_s3_bucket.dev_izybe_bucket]
  key        = "test_file.txt"
  source     = "test_files/sample_texte.txt"
  etag       = md5(file("test_files/sample_texte.txt"))
}