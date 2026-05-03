# Base Image: Use the official AWS MWAA base image. 
# Supported versions for custom images: 2.8.1, 3.0.6 (and later).
FROM public.ecr.aws/mwaa-base-images/mwaa-3.0:latest

# Set the working directory (optional, standard is /usr/local/airflow)
WORKDIR /usr/local/airflow

# Copy your local requirements.txt to the image
COPY requirements.txt .

# Install custom Python packages
# The --no-cache-dir flag helps keep the image size smaller
# Using --user is required by MWAA's execution environment
RUN pip install --no-cache-dir --user -r requirements.txt

# (Optional) Install system-level dependencies (must be done as root)
USER root
RUN yum update -y && \
    yum install -y \
    gcc \
    gcc-c++ \
    && yum clean all

# Switch back to the airflow user (MANDATORY for MWAA)
USER airflow

# (Optional) Pre-load plugins if you're not using plugins.zip on S3
# COPY plugins/ /usr/local/airflow/plugins/

# (Optional) Pre-load DAGs if you're not using S3 for DAGs (not recommended for most cases)
# COPY dags/ /usr/local/airflow/dags/

# (Optional) Custom Airflow configuration files # this is for that ecr new image change ...
# COPY config/airflow_local_settings.py /usr/local/airflow/config/airflow_local_settings.py
# COPY config/startup.sh /usr/local/airflow/startup.sh

# If you use startup.sh in the image, ensure it is executable
# USER root
# RUN chmod +x /usr/local/airflow/startup.sh
# USER airflow
