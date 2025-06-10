# compute

### ec2

Elastic Compute Cloud one of the most popular since under the hood many services use ec2, e.g.
rds, ecs, eks even though we can use fargate for serverless compute.
Even lambda which is serverless is running on an abstract layer of ec2.

- web service that provides us secure, resizable compute capacity in the cloud
- allows users to easily configure, launch and manage virtual servers, known as instances
- it provides on-demand, scalable computing capacity
- offers variety of instances with different combinations of conf (cpu, memory, storage, networking)
- users have full control over the configuration of their ec2 instances
- high availability deployed across multiple AZ and reliability (consistency, fault tolerance, availability, resilience,
  scalability support, monitoring and self-healing)
- auto scaling : automatically adjust number of instances in response to changes on the workload
- seamlessly integrates with other AWS services

- ec2 instances types
    - general purpose (provide a balance of compute, memory, networking resources, ideal for app that use such balance
      of conf like web servers and code repositories)
    - compute optimized (ideal for compute bound applications that benefit from high performance processors, e.g. media
      transcoding, high performance web servers, high performance computing, scientific modeling, dedicated gaming
      servers, ad server engines, machine learning inference ...)
    - memory optimized instances (designed for workloads that process large data sets in memory)
    - accelerated computing (use hardware accelerators or co-processors, to perform functions, calculation such as
      floating point number calculations, graphic processing, data pattern matching)
    - storage optimized (for workloads that require high and sequential read and write access to very large data sets on
      local storage)
    - HPC (high performance computing) optimized purpose built to offer the best price performance for running HPC
      workloads at scale on AWS (cluster) :
        - to process massive multi-dimensional data sets, also known as big data and can solve complex problems at
          extremely high speed
        - some large complex simulation
        - deep learning workloads
- hands-on : launch an ec2 with elastic ip and key pair so that we can connect to it

### aws batch

- run batch jobs on docker images (process large amount of data in one go and no needs to interact with it as a user)
- when to use it and what is the main differences between aws other services :
    - lambda :
        - lightweight, event-drive tasks
    - glue :
        - specialized for ETL, data integration service (also cataloguing ...)
    - batch :
        - versatile (can adapt efficiently), also can be used as data processing but in general more of a broad batch
          job computing
- features :
    - batch jobs based on docker images
    - automated scaling
    - can be scheduled
    - can be integrated with aws step functions
    - can be implemented retry mechanisms and also error handling
    - can be run as serverless service :
        - uses ec2 instances and spot instances
        - can be used together with fargate (is serverless so in this case we dont neet to manage infra)
        - no need to manage infrastructure
- pricing : based on the compute resources that used
    - ec2 instance, fargate, spot instance costs
    - measured in instance/hour (the compute time the job is running)
    - only paying for the ec2 instance running or fargate usage costs if we use fargate
- usage :
    - define the job (docker container, code, cpu, memory, job queue, and any dependencies ...)
    - submit the job to the job queue (with priority)
    - schedule the job
    - running on a compute environment

### SAM (serverless application model)

Framework to help create and manage infrastructure on AWS. Simplifies the deployment process of serverless application
like aws s3, lambda, dynamoDB ...

- YAML codification for the infrastructure (declarative instructions)
- integration tool with common IDE e.g. Pycharm, Visual Code, Intellij, ...
- provide a local development environment that mimics AWS (local debug and testing capabilities )
- eases the process of deployment
- provides command like :
    - sam build
    - sam package
    - sam deploy
- how to :
    - write the template with all the metadata and the definition of our resource
    - build the project locally ( sam build command, will translate to cloudformation-like template, download all the
      dependencies, ...)
    - package the project (code and dependencies) and upload to s3, then generate references to the uploaded artifacts (
      on s3)
    - verify the package and create a stack on cloudformation
- example of template to create a basic s3 :
  here the output is where to store the metadata of the cloudformation stack to make it available from other stack
    ```yaml
    AWSTemplateFormatVersion: '2010-09-09'
    Transform: AWS::Serverless-2016-10-31
    Description: A simple SAM template to create an S3 bucket
    
    Resources:
      MyS3Bucket:
        Type: AWS::S3::Bucket
        Properties:
          BucketName: my-sam-s3-bucket-example
    
    Outputs:
      BucketName:
        Description: Name of the S3 bucket created
        Value: !Ref MyS3Bucket
    ```

### application autoscaling

application autoscaling helps us to automatically scale our scalable resources :

- dynamoDB
- amazon aurora
- sagemaker
- aws managed streaming for apache kafka (MSK)
- aws neptune, emr ...

for better performance and cost savings : in order to not over-provision our resources during low traffic periods
also performance assured during high traffic workload

2 different types of autoscaling :

- schedule based : e.g. predictable peak of workload pattern like each monday morning
- target tracking policies based : set a target policy based on metric target
    - how to :
        - choose a metric and set a target value (can be custom or predefined of combined)
            - e.g : like 50 percent CPU utilization
        - this would create cloudwatch alarm to trigger the auto-scaling when the limit is reached (when the metric
          deviate from the target)

[<<Home page](./../README.MD#compute)