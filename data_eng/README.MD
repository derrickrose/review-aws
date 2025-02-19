# data eng

[Udemy course](https://www.udemy.com/course/aws-certified-data-engineer-associate-dea-c01/?couponCode=BFCMSALE24FRTR)

## glue

- managed etl
- data catalog (centralized data schema backed by metadata)
- crawlers (scan and infer schema) e.g. semi structured data (csv, json, ...)
- structured as base and table
- [Glue deep dev](./glue/README)

## athena

- query service
- federated queries (from different data source e.g. dynamo, documentdb, rds ...)
- performance and cost
- for performance it uses partitioning (using dates for example)
- for performance too it uses partition projection (unlikely to be used during the query so skipped)
- workgroup (like workspace)
- athena query result s3 bucket
- can specify limit of data queried on workgroup

## aws budget

Inside billing and cost management service

- set alarms when exceeded
- actual and forecast (help manage cost)
- budget types :
    - Cost budget
    - Usage budget
    - Saving plan budget
    - Reservation plans budget
- cost of budget
    - 2 action-enabled free then it is 0.1 per day

## aws lambda

- used for data ingestion and data processing (basically stateless ingestion because every execution is independent)
- lambda is a serverless service which allow to run code without caring about the infrastructure
- automatically scaling based on demand
- various programming languages such as python, java, go, node.js
- cost efficient (pay only what you use)
- use cases :
    - data processing (data in s3 or DynamoDB)
    - event-driven ingestion (responding to some events from s3, dynamoDB, kinesis)
    - automation (automate tasks and workflows by triggering lambda functions in response to events)
    - examples :
        - s3 notification event (on file upload) => trigger the lambda function (which runs the code) => transferring it
          to another bucket
        - kinesis data stream set as event source => trigger the lambda => execute the code on a continuous manner (each
          100 records then execute the code)
- lambda layers :
    - contains supplementary code:
        - library dependencies
        - custom runtime or
        - configuration file
    - example function1(functionCode1, customDependencies, conf) function2(functionCode2, customDependencies, conf)
      repetition
    - ==> the solution is to use layer :
        - packaging the customDependencies and the conf in a zip file
        - create the layer in lambda
        - add the layer to the function
        - the function can access the contents of the layer during runtime
    - benefits :
        - share the dependencies across multiple functions
        - separate core logic from dependencies
        - reduce package size

## data streaming in aws

- re-playability : the ability to re-process already processed data
    - why?
        - because there could occur errors when processing it at first (ability to re-drive)
        - data consistency (synchronized and correct, ensures uniform data across distributed systems)
        - adapting to changes: adjusts to schema or source data changes
        - test and development: facilitates feature testing and debugging without risking live data integrity
    - how to implement it
        - idempotent operations: ensure repeated data processing yields consistent results
        - logging and auditing : keep detailed records for tracking and diagnosing issues
        - checkpointing : use markers for efficient data process resumption (bookmarks)
        - back-filling mechanisms : update historical data with new information as needed

- [Kinesis for streaming data](./kinesis/README.MD#kinesis)

- Amazon MSK (Amazon Managed Service for apache Kafka)
    - aws managed real-time data handling
    - need setup (custom configuration and scalability)
    - distributed architecture (use of brokers)
        - brokers are servers that manage the publishing and subscribing or records
        - zookeeper nodes : coordinates Kafka brokers and manages cluster metadata
    - multi-AZ deployment
      EBS (elastic block storage) for storing data
      also works as producers / consumers mode (like kinesis)
      kinesis vs MSK

      | MSK                                                   | Kinesis                                                                  |
                                                                                                                                                   |-------------------------------------------------------|--------------------------------------------------------------------------|
      | customizable message size up to 10MB data throughput  | convention and up to 1MB data throughput limit                           | 
      | more complex pipelines                                | straight-forward setup                                                   | 
      | topics and partitions                                 | streams and shards                                                       | 
      | scaling means adding partitions but cannot be removed | adjustable throughput, scaling means adding shard but can be merged also | 
    - Security :
        - MSK
            - in flight TLS encryption or plain text
            - at rest : supports KMS encryption
            - Access control :
                - mutual TLS
                - SASL/SCRAM username/password authentication mechanism, also relying on Kafka ACLs
                - IAM access control authentication and authorization using IAM
        - Kinesis
            - in flight TLS encryption by default
            - at rest : supports KMS encryption
            - Access control :
                - uses IAM policies for both authentication and authorization
    - MSK Connect and MSK serverless:
        - MSK Connect :
            - similar to Kafka Connect connectors (to simplify kafka integration /connection to other systems)
            - to connect MSK to external services
            - fully managed service (auto-scaling connectors)
        - MSK serverless :
            - automates capacity management, focusing on throughput and storage needs without manual scaling

## s3

[simple storage service](./s3/README.MD#s3)

- naming convention
- storage class
- availability zone related
- bucket name uniqueness
- versioning

data ingestion

- stream
    - time sensitive
- batch
    - cost effective

## other storage

[other storage](./other_storage/README.MD#other-storage)

## dynamodb

[dynamodb](./dynamodb/README.MD#dynamodb)

## redshift datawarehouse

[redshift](./redshift/README.MD#redshift-datawarehouse)

## rds

[rds](./rds/README.MD#rds)