# rds

fully managed relational database system

- main characteristics : scalable, reliable, cost effective
- fully encrypted at rest or in transit
- support multiple database engines :
    - mysql
    - postgreSQL,
    - sql server, mariadb,
    - oracle
    - aurora
- security in rds:
    - run instance in VPC (for isolated environment)
    - choose to encrypt or no data (at rest or in transit)
    - patch management automatic  (automatic minor version upgrades for minor updates
    - backup , centralization and automation of data backup or manually
- RDS is following the ACID compliances :
    - atomicity : transaction is all or nothing, (if a part fail so rollback)
    - consistency : after a transaction, data should be consistent an so are the constraints ...
    - isolation : transaction made is not visible until it is completely done
    - durability : data should be persisted event after computer restart, failure ...
- additionally special future locks
    - locks are automatically used by the db during transactions but it can be managed by user
    - locking mechanisms for concurrent data access and modification in multiple transactions to make sure everything
      run fine
    - different lock mechanism :
        - exclusive locks (prevent other transactions from reading or writing to the same data)
            - syntax : LOCK TABLE table_name IN EXCLUSIVE MODE
        - shared locks (prevent from writing to the data but can reading)
            - syntax : LOCK TABLE table_name IN SHARED MODE
        - tables and rows used for data integrity and control
        - syntax and deadlocks :
            - postgres command to lock a table
                - LOCK TABLE table_name IN ACCESS EXCLUSIVE MODE (generally used for query which make changes on table
                  structure e.g. adding a column)
            - to acquire a shared lock
                - SELECT * FROM table_name FOR SHARE;
            - to acquire an exclusive lock
                - SELECT * FROM table_name FOR UPDATE; (select rows with the intention to update them)
            - deadlock waiting on other transaction to complete but actually depends on each other

### best practices

- monitor metrics for memory, CPU, replica log and storage via cloudwatch
- scale database instances to manage storage capacity efficiently
- enable automatic backups during periods of low write IOPS
- provision sufficient I/O capacity for your database workload
- set a time-to-live (TTL) value under 30 seconds for cache, since app is using DNS to get the IP address and if the TTL
  value is so high, it may not have the correct IP after a fail over
- conduct a fail over testing regularly
- allocate enough RAM, so that your working set (data and indexes that are frequently used in your instance) resides
  almost completely in memory ==> how to do?
- check the read IOPs metrics constantly, when instance is under load (cloudwatch) (value should
  be small and stable)
- use enhanced monitoring to obtain real time metrics for the OS in your DB instance
- use performance insights for RDS and Aurora
    - simplifies database performance monitoring and tuning
    - easy to use dashboard
    - example of use => detect performance issues
    - evaluate impact of SQL queries and optimize them (dev and test)
    -
- mysql : ensure tables don't exceed the 16TiB size limit by partitioning large tables
- oracle FlashGrid cluster : utilize virtual appliances to run self-managed RAC and RAC extended clusters across AZs aon
  EC2 (full control using FlashGrid and operating system level access)
- RDS for postgreSQL : improve performance by optimizing data loading and utilizing the autovacuum feature effectively
- SQL Server fail over : allocate sufficient provisioned IOPs to handle your workload during fail over

### amazon Aurora

- fully managed RDBMS made by AWS
- fully compatible with full mysql and postgresql
- easy transition from mysql and postgresql
- performance up to 5 times of mysql and 3 times of postgresql
- scales from 10GB to 128TB as needed
- read replicas : upt to 15 replicas to extend read capacity
- security : IAM for authentication, supports encryption at rest and in transit
- feature Aurora serverless :
    - automatic scaling : auto-adjust to the application's needs (no manual scaling required)
    - on-demand usage : pay for what you use is ideal for sporadic or unpredictable workloads
- simple setup : no management of database instances, automatic capacity handling
- cost-effective : bills based on Aurora Capacity Units (ACUs), suitable for fluctuating workloads

### amazon DocumentDB

- fully managed NoSQL database service
- document-oriented
- fully compatible with mongoDB
- serverless, managed service (aws handles provisioning, setup etc ...)
- high availability and durability (built on aws infrastructure with multi-AZ replication)
    - replicates 6 copies of data across 3 availability zone and continuously back up on s3
- security : IAM authentication, supports encryption at rest and in transit
- pricing :
    - instance hours : charged based on instance run time
    - storage & I/O: fees for s3 storage and I/O operations
    - backup storage : additional cost for backups beyond free retention limits

### amazon neptune

- fully managed graph database
- optimized for highly connected datasets
- use cases :
    - knowledge graphs (wikipedia)
    - fraud detection
    - recommendation engines
- data model :
    - property graph : vertices (nodes) and edges model
    - RDF (resource description framework) : triple-based model for efficient data querying
- fully managed
- high availability : across 3 AZs, supports automatic failover
- secure : uses AWS KMS for encryption, provides VPC isolation
- scalability : auto-scales to 64TB up to 15 read replicas
- fast and reliable : handles billions of relations with millisecond latency
- integration :
    - AWS ecosystem : integrates with lambda, s3, sagemaker
    - open standards : complies with Gremlin and SPARQL
- performance : query optimization, advanced techniques for graph traversal
- concurrency and throughput : optimized for high traffic
- pricing : based on instance size and usage hours
- complexity : demands graph database knowledge
- specialized : focused on graph-specific applications

### amazon keyspaces (for apache cassandra)

- fully managed NoSQL database
- fully compatible with apache cassandra
- fully managed (serverless)
- high availability and durability (across multiple AZ)
- IAM for authentication, supports encryption at rest and in transit
- pricing :
    - on demand capacity : pay for throughput and storage
    - provisioned : for predictable workloads

### amazon memorydb for redis

- fully managed in-memory database service (for low latency and high throughput access)
- fully compatible with redis, supporting redis API and data structure
- automatically scales to adapt to workload changes
- durability : ensure data persistence with snapshotting, spread to multiple availability zones
- security : IAM for authentication, support encryption at rest and in transit
- use cases :
    - caching
    - leaderboard an counting (gaming and social networks)
    - session store: for web app ensuring fast retrieval and persistence
    - node pricing :
        - charges based on type and number of CPU, varying by cpu, memory and network perf
        - charges on data transfer (in and out), intra region transfer typically not charged
        - charges on backup storage beyond three-tier
    - reserved instances : available for long-term use at a significant discount, with one or 3 years commitment

### amazon timestream

- fully managed serverless time-series database
- designed for high-performance real-time analytics
- basically for data with timestamp
- used for measuring data that change over time
- uses cases :
    - iot applications
    - application logs
    - devOps monitoring
    - financial market data
- features :
    - serverless
    - optimized for time-series data
    - time series specific functions
    - high performance time series
- examples of usage :
    - ingestion from
        - lambda (may be transform before ingest can be from api or webhook or some other trigger),
        - amazon msk (for real time streaming or realtime analytics),
        - managed apache flink (real time aggregation),
        - kinesis data stream, iot core to connect to iot device
    - then comes the ingestion to amazon timestream
    - then the output :
        - managed grafana (analysing metrics and logs)
        - quicksight
        - sagemaker
        - or may be other devices using JDBC driver
    - concrete example real-time processing with Iot devices (monitoring on iot devices)
        - iot devices (generate data) >> kinesis data stream (transport streaming events) >> managed apache flink
          (transforming data since they can be different format, detect error) >> timestream >> managed grafana (
          visualize metrics and logs)
        - additionally from kinesis data stream >> we can redrive data to firehose then >> :
            - process with lambda
            - store to s3 for datalake

[<<Home page](./../README.MD#redshift-datawarehouse)