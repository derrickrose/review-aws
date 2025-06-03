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

[<<Home page](./../README.MD#compute)