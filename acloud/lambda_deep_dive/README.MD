# AWS Lambda deep dive

## Serverless

Just write code, no need system config, patch update, security

## Lambda service

Lambda function is the function definition along the configuration which will be initialized and called by the lambda
service

#### Function configuration

Set the code, required performance, concurrency limits, permissions, storage, link directly to event sources ...

#### Lambda service

Initialize and call the lambda function and handles inputs/outputs, load balance, route and poll event sources

#### Runtime

Environment that provides all resources the lambda function requires to be executed (programming language, libraries,
operating system)

- supporting programming language like go, ruby, .net, java, python, node.js
- How it works? On invocation, lambda service creates a runtime instance which contains your function code and the
  runtime is responsible for sending the input events and the context to the function code
- **runtime updates:**
    - default and recommended: **auto** (aws automatically makes updates, security, os ...), the rollout is made in 2
      phases; first the update is applied when functions are created or updated and in second part it may get applied to
      the remaining runtime
    - function update: the updates are made only when you make a change to your function
    - manual
- **runtime deprecation:** !! you should update but execution will not be blocked!!
    - creation with that specific version is blocked
    - a month later, updating blocked
    - a notification will be sent 120 days before the deprecation by a trusted adviser
    - an email will be sent to customer 60 days before the deprecation
- **specific environments** can be configured for certain runtimes to inject additional functionality, example the use
  of JAVA_TOOL_OPTIONS to inject java agent for telemetry, NODE_OPTIONS trace-warning to show a full trace of each
  warning, DOTNET_STARTUP_HOOKS to inject logging
- **another option for modifying the supported runtimes** is to use a wrapper script, the wrapper script is executed
  first then the lambda handler be called. The ability to run script before the handler invocation might help to change
  the startup behavior, run shell commands, inject arguments, capture errors and metrics, execute binaries, but only
  supported by native runtime, use environment variable AWS_LAMBDA_EXEC_WRAPPER to point to executable binary
    - use of custom runtime : add non-supported programming languages as bash, c, rust... performance reason (example go
      does not support processor graviton)
    - how to use it:
        - first configure the lambda to use the provided.al2 runtime (amazon managed operating system)
        - include an executable script called boostrap along with the function or within a lambda layer
        - the bootstrap file should define the initialization tasks such as starting an event loop for processing
          events, should use environment variable like where is set the handler, and details where calling the lambda
          runtime api
        - the runtime must call hte lambda runtime api to retrieve events and process them, a call should be made to the
          runtime api to return
          response or errors handling
- processor: to understand the use of processor, you should understand ISA (instruction set architecture interface
  between hardware and software which defines how the CPU is controlled by the software)
    - x86_64 very common (example pc)
    - arm64 (example tablets, phone, macbook M1) cheaper but not always compatible and can be giving more performance
      for certain workloads (example aws graviton2 processor is using this architecture), (Not supported by python3.7,
      .net5.0, go1.x)

## Event-driven

Executed as a response to an event, example of events :

* updates to dynamodb table
* data streaming via kinesis
* rest api requests
* infrastructure notifications
* object upload to s3 buckets

## Storage

## Invocation

#### Synchronous

- Calling application make request and wait until the lambda function returns a result
- The lambda service route the request to an availability zone (AZ), initializes the function and executes it
- If another call is made, the function already been initialized, it might be reused but routed to another AZ

#### Asynchronous

- The lambda service put the request in a queue and returns immediately a response to the calling application
- Then executes every queued requests
- The response to the executions can be routed to output services such SNS, SQS, EventBridge bus or even another lambda

- **EVENT SOURCE MAPPING pattern:** lambda service can handle mapping events from source such as : SQS queue, SNS topic,
  DynamoDB stream, Kinesis stream, MQ, Apache Kafka, DocumentDB
    - Event source mapping invocation: an event source is configured, lambda service will poll events from source, group
      in
      a batches, filters based on your conf, initializes the function and invokes the function with the events as an
      input
    - Response can be routed to an output service such as SNS, SQS and more

## Limits

- 15 minutes limit for single execution

## Cost

No subscription needed, pay per request and per execution duration

## Use and Misuse

#### Use

- transforming data
- file processing
- website backend logic
- generating reports from dynamodb item changes
- processing IoT data
- automated remediation (roll back to default security if a breach is found)
- schedule tasks
- **Examples:**
    - backend endpoint for adding item to basket, deleting item from a basket
    - creating a thumbnail of an image and upload it to a website then store the path to a dynamodb table
    - cctv camera publishing notification to an SNS service, lambda can save pic to s3 bucket, another lambda can record
      the time of sighting to db, third lambda that utilises AI service to identify the dog

#### Misuse

- long-running tasks
- constant workload (many requests at constant rate) can be very expensive
- large code base
- long term state
- anti-pattern monolithic application (for multiple use)
- recursion (take precaution endless loop as an event same s3 bucket for event source and output destination)
- complex workflow logic (might better delegated to step function)
- chaining (lambda call another lambda that call another lambda)
- waiting (as an example if the code waits request from a database and an external api, might be better to use
  asynchronous calls to avoid unnecessary delays)
