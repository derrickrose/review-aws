# Glue deep dive

- glue cost
    - crawlers based on number of DPU (data processing unit) (4vCPU and 16 GB)
        - hourly based cost (example half an hour)
        - billed by seconds with minimum of 10 min
    - data catalog
        - up to 1 million object free
        - 1 dollar per 100 mil objects over a million per month
    - ETL job also based on number of DPU
        - 0.44 dollar / hour
        - billing by seconds with 10 min minimum
        - starting from version 2 , cost by second and minimum of 1 min
        - how many DPUs are used ?
            - Spark under the hood (minimum 2 default 10)
            - Spark streaming minimum 2 default 2
            - Ray job (ML/AI) minimum 2 M-DPUs (high memory) default 6
            - Python Shell Job (flexible and simple not distributed) default 0.0625 DPU
    - Cost of DPU
        - 0.44 dollar per DPU-hour (may deffer and depend on region)
    - Glue Job Notebooks / Interactive Sessions (used to interactively develop ETL code in notebooks)
        - based on time session is active and number of DPUs
        - configurable idle timeouts
        - 1 min minimum billing
        - minimum 2 DPUs and default 5 DPUs

    - ETL jobs cost examples
        - apache spark job runs 15 min uses 6 DPUs
            - ==> 6 DPUs * 1/4 (hour) * 0.44 = 0.66 dollars
        - interactive notebook sessions 24 minutes with default 5 DPUs
            - ==> 5 DPUs * 2/5 (hour) * 0.44 = 0.88 dollars

- [setting budget](./../README#aws-budget)

- run glue job
    - glue provides a visual job editor
    - creating an s3 to s3 load job; select a folder as source also another folder as destination
        - defining the source and target files format
        - data catalog update options
            - not update the catalog
            - create a table in data catalog and update schema and partitions on subsequent runs
            - create a table in data catalog, keep schema but update partitions only
        - need to create iam role for the job, do not forget to add up permissions for reading and putting into s3
          buckets

- scheduling crawler and glue job
    - from job details there is a section schedule
    - define frequency  (daily, monthly, ...)
    - can add multiple schedules

- stateful and stateless data ingestion
    - Amazon kinesis support both stateful and stateless data processing :
        - stateful data streams
        - stateless firehose
    - aws glue provides stateless and stateful processing by job bookmarks
        - stateful (active bookmarks on job details section) for tracking progress
        - stateless (does not activate bookmarks)
        - bookmarks can be paused too
        - hands on for stateful ingestion :
            - with the same etl load s3 to s3, activate bookmark, add some csv files, run the job, it will process only
              new data

- glue transformation ETL
    - Extract
        - Amazon RDS, Aurora, DynamoDB
        - Amazon Redshift,
        - Amazon S3, Kinesis
    - Transform
        - Filtering : remove unnecessary data
        - Joining : combine data
        - Aggregation : summarize data
        - FindMatches ML: Identify records that refers same entity (e.g. find matches between a competitors data)
        - Detect PII : identify and manage sensitive information (e.g. payment card, social number id, ...)
        - transform format (CSV <-> PARQUET (analytics columnar) <-> JSON <-> XML ...)
    - Load
        - Amazon RDS, Aurora, DynamoDB
        - Redshift
        - S3, Kinesis

- data quality
    - set of quality rules
        - e.g. column count should be 7 columns
    - can use machine learning to identify unusual patterns in data
    - can be applied to data at rest or in transition with the ETL pipeline

- glue workflow
    - provides editable visual interface of the workflow
    - orchestration within glue (manage triggers, component integrations, basically the operations)
    - for more complex orchestration, better option use step function
    - can be created using aws glue API, visual editor, glue blueprints (python code of config template)
    - creating a workflow from the visual interface then add a trigger first
    - trigger types and examples :
        - event : example run crawler when glue job is successful
        - EventBridge : respond to a specific event within AWS EventBridge
        - on demand : manual trigger or other services like step function or lambda
        - schedule : periodically or using cron jobs
    - each component should be associated to a trigger :
        - for example the on-demand workflow starting point trigger runs the first job
        - if we need to add up another job, we need to add up a new trigger (the new trigger can be the success of the
          previous job)
    - possibilities :
        - put conditional run of a job for example if the previous task run is failed, run another different job (
          branching)

- glue job types
    - way of creating a glue job
        - visual ETL (it will create a spark job under the hood)
        - notebook (interactive session)
        - script editor (creating script from scratch), some available options out there :
            - spark
            - ray (ml)
            - python shell
    - spark glue etl jobs
        - large scale data processing
        - default 10 DPUs, min 2 DPUs up to 100 DPUs
        - suited for big data workload
        - each DPU include 4 vCPUs and 16 GBs of memory
    - spark streaming ETL job
        - analyze data in real-time
        - default 10 DPUs, minimum 2 DPUs up to 100 DPUs
        - works with streaming data sources like kinesis data streams and Kafka
    - python shell job
        - suitable for light-weight data driven transformation tasks (no need complex spark env)
        - default 0.0625 DPU to 1 DPU
    - ray job (python native) (run on new graviton EC2 computers not spark)
        - suitable for parallel processing tasks (workload on hundreds of data sources, or machine learning; for large
          scale python process)

- execution types
    - standard execution
        - designed for predictable ETL jobs
        - jobs start running immediately
        - guarantees consistent job execution time
    - flex execution
        - cost effective option for less time-sensitive ETL jobs
        - jobs may start with some delay (job are queued and then run on some available resources later)

- partitioning (#TODO practice)
    - with partitioning we organize data in an efficient way based on some conditions
    - we set partitioning as file locations for example in s3 bucket (for large data) after the data processing being
      done
        - example of partition by date :
            - data/
                - partition1_year=2024/
                - partition2_year=2023/
    - it helps reduce cost since query on athena would be pointed directly to the related appropriate/relevant partition
    - by that, will perform better querying on data
    - also glue can process partitions independently
    - define partitioning as part of ETL job scripts, then also possible within glue data catalog
    - with crawlers can directly recognize those partitions if the data is properly organized like the example

- glue DataBrew (like excel)
    - used for data preparation (cleaning, format, basically pre-processing data)
    - can be part of etl transformation but also can be used with machine learning
    - visual interface (no-code)
    - 250+ pre-built transformations
    - schedule and automate repetitive tasks
    - can be integrated with other aws services (s3, redshift, lakeformation)
    - DataBrew concept :
        - project (where to configure transformation tasks)
        - step (applied transformation to the dataset)
        - recipe (sets of transformation steps, can be saved and reused)
        - job execution of a recipe on a dataset, output to location such as s3 for example
        - schedule job to automate transformation
        - data profiling to understand quality and characteristics of the data
    - examples of DataBrew prebuild transformation
        - **NEST_TO_MAP** convert columns into map

          |     Name     |    Age     |           City            |
                                                                                |:------------:|:----------:|:-------------------------:|
          |    frils     |     37     |         boulogne          |
                 => {"Name":"frils", "Age":"37", "City":"boulogne"}
        - **NEST_TO_ARRAY**

                => ["fril","37","boulogne"]
        - **NEST_TO_STRUCT**

                => like NES_TO_MAP but retains exact data type and order
        - **UNNEST_ARRAY** (same as UNNEST_MAP...)

                => transforms array to table 
        - **PIVOT** pivot column and pivot values to rotate data from rows to columns
        - **UNPIVOT** pivot column into rows

                => 
          | Attribute | Value |          
                              |----------|------|
          |      Name | frils |   
        - **TRANSPOSE** changing columns into rows

                =>
          | Attribute | frils |          
                              |---------|-----|
          | Age | 37 |   
          | City | boulogne |
        - join combine 2 datasets
        - split column into multiple columns based on delimiter
        - filter to keep only specific rows in the dataset
        - sort arrange the rows in ascending or descending order
        - date/time conversions convert string to date/time formats or change between different date/time formats
        - count distinct
    - pricing
        - interactive session are billed per session (30 minutes each)
        - first 40 interactive sessions are free then 1 dollar per session
        - job are billed per minute, 0.48 dollars per node hour
    - applying transformation can be done by selecting a column and apply to it the transformation to do or in the
      project explorer in the right then add a step
    - any step can be previously previewed too

[<<Home page](./../README.MD#glue)