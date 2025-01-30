# kinesis

- cost :
    - 0.015 dollar per hour
    - PUT payload units : 0.014 per 1 000 000 units

- collection of services to handle data streaming in aws :
    - kinesis data streams :
        - ingest and process large volumes of streaming data (highly scalable)
    - kinesis data firehose :
        - fully managed service to deliver data to different destinations : s3, amazon redshift, amazon elasticsearch
          service, splunk
    - managed apache flink (formerly kinesis data analytics)
        - analyse streaming data in real time using standard sql queries (sent by kinesis or firehose)

- use cases : variety of real time data processing and analytics use cases
    - real time analytics : analyzing streaming data to gain insights
    - iot processing : ingesting and processing data from iot devices or sensors
    - security and fraud detection : detecting anomalies and responding to security in real time

- kinesis data streams :
    - producer : device or application generating data streams
        - create producer :
            - with aws sdk, customizable
            - kinesis producer library (KPL) when we have a high throughput data application and need to send data to
              kinesis efficiently (KPL handle errors and batching of records which leads to higher throughput)
            - amazon kinesis agent (pre-build app) for log data to ingest
        - the producers write data to data streams (and data stream is composed with different shards)
            - the producers format data to data records (unit up to 1MB of data, e.g. json object or log)
            - includes partition key, associating a record to a shard
            - how does a shard look like ?
                - basic unit of capacity 1MB/s or 1000 records/s in-throughput / 2MB/s or 2000 records/s out-throughput
                - with those shots we have the numbers of shards and the capacity of the ingestion
                - => basically a shard is processing unit that provides a fixed amount of data throughput
            - a data from stream can last 24 hours in default, but the retention period is configurable to up to 365
              days
            - data in streams are replicated across different availability zones in order to be durable
            - resilient
            - immutable
            - scalability (auto)
            - capacity mode :
                - provisioned mode :
                    - must specify the number or shards;
                    - pay hourly
                - on demand mode :
                    - automatically scales shards based on throughput peaks over las 30 days
                    - default : 4MB/s or 4000 records
        - and then send records to consumer; to create consumers :
            - same as producer, can use aws sdk, KCL (Kinesis Client Library)...
            - different consumer services :
                - load data to different location using kinesis data firehouse
                - managed apache flink
                - lambda
                - other services

- throughput and latency
    - volume of data (MBps or records per seconds) ingested into or retrieved from Kinesis Data Stream
    - real-world : actual rate of data processing, accounting for all factors
    - shard-based scaling : scalable through number of shards, each shard adds fixed capacity to stream
    - proportional relationship : total stream throughput directly relates to shard count
    - optimization goal : improving capacity to process more data within timeframe for high-volume data

- bandwidth
    - the maximum data transfer rate
    - theoretical upper limit : potential maximum for throughput

- latency :
    - the time from initiating a process to the availability of the result
    - propagation delay : specific latency from when a record is written to when it's read by a consumer
    - influencing factor : polling interval : how often consumer applications check for new data (recommendation check
      shards in the stream once per second per consumer)
    - KCL library defaults :
        - configured to poll every second, keeping average delays below one second
        - reducing delays for immediate data needs :
            - increase the KCL polling frequency for quicker data access, with careful management to avoid API rate
              limit issues (reduce latency to less than one second for e.g.)

- Enhanced fan-out for kinesis consumers
    - fan out : a single stream distributes data to multiple consumers (distribute data to different applications)
        - traditionally : shared through-put (standard consumer), potential bottleneck
        - solution : enhanced fan-out (push data through http/2) and each registered consumer have its own dedicated
          read throughput (up to 20 consumers)
        - each consumer up to 2MB/second per shard (=> 10 consumers lead to 20MB/s of throughput instead of 2 from the
          standard)
        - increased scalability : the system using this can handle more concurrent consumers without performance
          degradation
        - reduced latency (~70ms)
        - simplified application development: don't need to implement complex logic to manage shared throughput between
          consumers
        - when to use it? :
            - higher cost
            - high number of consumers
            - require reduced latency
    - fan in : multiple sources converge their towards a single destination (destination can be another stream or
      storage; e.g. combine data from different sensors into a single stream)

- pull and consume data from stream (hands on):
    - put record to the stream using cloud shell:
        - ```
          aws kinesis put-record --stream-name YourStreamName --partition-key "PartitionKey" --data $(echo -n "Data
          Entry 1" | base64) 
          ```
    - to consume, we use shard iterator is like a pointer to point which part of the stream we would like to consume
    - get the latest shard iterator, the way to do is mention the shard id :
        - ```
          aws kinesis get-shard-iterator --stream-name YourStreamName --shard-id "shardId-000000000000"
          --shard-iterator-type LATEST
          ```
    - get a record using the shard iterator id (returned from the previous command) :
        - ```aws kinesis get-records --shard-iterator "YourShardIterator"```
        - this will return actual records and then the next iterator id
        - note : to get the oldest iterator (old data) with this command :
        - ```
          aws kinesis get-shard-iterator --stream-name
          YourStreamName --shard-id "shardId-000000000000" --shard-iterator-type TRIM_HORIZON --query 'ShardIterator'
          --output text
          ```
    - consume data using lambda function :

- common issues and troubleshooting :
    - slow write rates
        - problem : service limits and throttling (may writing data exceeding stream capacity or API rate limits)
            - for example create stream or delete stream (it has limit of 5 to 20 calls per second)
        - solution : monitor throughput exceptions
    - uneven data distribution to shards (hot shards)
        - problem : all records are being sent to one shard for example
        - solution : effective partition key strategy
    - high throughput and small batches can be inefficient
        - solution : batch records to aggregate multiple records
    - slow read rates
        - problem: hitting shard read limits (per-shard limit)
        - solution: increasing shard count
        - problem : low value for maximum number of GetRecords per call
        - solution : System-defaults value are generally recommended
        - problem: logic inside ProcessRecords takes longer than expected
        - solution : change logic, test with empty records
    - other common issues :
        - GetRecords returns empty records array
            - solution : every call to GetRecords returns a ShardIterator value (must be used in the next iteration)
            - empty records reason :
                - no more data in the shard
                - no data pointed to by the ShardIterator
                - it is not an issue and usually automatically handled by KCL (Kinesis Client Library)
        - records are skipped
            - solution : might be due to unhandled exceptions => handle all exceptions
        - expired shard iterators
            - dynamodb table used by kinesis does not have enough capacity to store the data, large number of shards
            - solution : not called GetRecords for more than 5min, increase write capacity to shard to table
        - consumer falling behind
            - => solution : increase retention
            - monitor GetRecords.IteratorAgeMilliseconds or MillisBehindLatest metrics
                - Spikes : API failures (transient)
                - Steady increases : Limited resources or processing logic
        - unauthorized KMS master key permission error
            - problem : writing to an encrypted stream without the necessary permissions on the KMS master key
            - solution : ensure you have the correct permissions via AWS KMS and IAM policies

- kinesis data firehose
    - automates data streaming and loading, reducing the needs of manual setup and administration
    - used to deliver data to another amazon services effortlessly: s3, redshift (indirect via s3), opensearch,
      splunk or mongodb
    - consume data from several services (cloudwatch logs, cloudwatch events, data stream, logs from iot, ...)
    - fully managed service (no need to code like in data stream nor setup any shard)
    - near real-time : propose a buffering (time related up to 900 seconds or size related up to 128 MB), then deliver
      the data (thanks to CDF connected device framework <=> many microservices)
    - auto-scaling
    - reliability : can re-drive data to fallback s3 bucket in case of error then data can be re-processed (archive
      original records and can handle retry)
    - transformation with lambda
    - handle several format (json, parquet, ORC), encryption (KMS) and compression

- kinesis data stream vs kinesis firehose :

  | kinesis data stream                                                | kinesis data firehose          |
                |--------------------------------------------------------------------|--------------------------------|
  | need coding consumers/producers                                    | effortlessly                   |
  | need setup (shards)                                                | fully managed                  |
  | real-time (latency of 200millis or 70millis when enhanced fan out) | near real-time (use buffering) |
  | retention period 24 hours up to 365 days                           | no storage                     |

- kinesis firehose hands on
    - source data stream and deliver to s3
    - source data stream, transform using lambda and deliver to s3

- amazon managed service for apache flink (AMS Flink)
    - low latency , almost real time data analysis and data transformation (aggregation, ...)
    - fully managed (serverless and scalable)
    - integration with several programming language for query (java, python, sql, scala)
    - stateful (maintain the states) :
        - checkpoints and snapshots ensuring fault tolerance very interesting for anomaly detection
    - use cases :
        - real time anomaly detection (send alert or trigger an event based on data analysis for e.g.)
        - fraud detection
        - metrics analysis (real time monitoring e.g. website traffic realtime)
    - how it works :
        - flink sources (some data streams) : integration with s3, kinesis data stream, MSK, custom data sources (using
          connector or API)
        - on-the-fly processing (filtering, aggregating, ) using flink streaming engine
        - flink sinks : Kinesis data stream, s3 , amazon msk, custom data sources or some other analytical tools
    - price : pay as you go
        - kinesis processing units (KPU) , 1KPU = 1vCPU and 4GB of memory
        - each application requires one additional KPU por orchestration (in our charge)
        - storage and backups (per GB per month)
        - auto scaling : number of KPUs automatically scaled based on needs, but can provision manually
        - AMS Flink Studio (Interactive Mode) : charged for 2 additional KPUs (like notebook)

[<<Home page](./../README.MD#data-streaming-in-aws)