<a id="dynamodb"></a>

# dynamodb

### intro

relational db :

- structured data in tables
- require fix schema (columns and rows)
- vertically scalable scale up (more subject to limits)
- sql queries (complex sql queries possibles) (joins, aggregations, ...)
- reporting, transactions in financial system, ...

nosql db :

- structure, semi-structured and unstructured
- no need for fix schema (schemaless) => can add data on the fly; example in document db, we can add nested json on the
  fly
- horizontally scalable => scale out (distributed)
- varying ways of querying (no joins, no aggregations)
- optimized for performance (large volume & flexibility)
- big data, real-time analytics

### overview

- dynamodb is a nosql db (not only sql) / non relational
- supports both key-value and document data model
- fully managed distributed database (everything is managed, patch, scaling, ...)
- perform very well under high traffic and high workloads
- high-availability and durability through distribution and availability zone replication :
    - easily scalable and can also be done automatically
    - all data are stored in SSDs
    - dynamodb automatically spread the data
- supports encryption at rest
- millisecond latency

### hands on (create a table)

- no rows in dynamodb but we have items instead
- partition key is the unique id and is also responsible for allocating the data across different hosts
- sort key is like a second part of the primary key (so we can have several items with same partition key but different
  sort key)
- under table > create table > table name > partition key (unique id) > table settings > table class > capacity
  calculator (provisioned/or On-Demand > have to specify how much read and write needed) > secondary indexes (for
  specific access pattern or example we often collect data from one category which is different from our partition key,
  this is to increase the performance) > encryption

### core components of dynamodb table

- tables (a collection of data)
- items (like row in relational db)
- attributes properties of a table
- each tables in dynamodb should have a primary key
  example table book :
    - primary key is book_id
    - table is schemaless (here apparition of new attribute publisher in the second JSON on the fly )
    - nested attributes are possible
    - each attribute's value is scalar (only one value)

```json
{
"book_id" : "b1",
"title" : "the great adventure", 
"author" : "Ella Fitzgerad", 
"price": 9.99, 
"genre": ["adventure", "fantasy"],
"publish_year": 2010
}

{
"book_id" : "b2",
"title" : "cooking simplified", 
"author" : "James Oliver", 
"price": 20.00, 
"genre": ["cooking"],
"publish_year": 2015,
"publisher": {
"name": "Yummy Books", 
"Location": "New York"
}
}
```

### creating items (hands on)

select our table > create item > add new attribute > ...

- partition key cannot be changed, it is fixed once upon on creating the table
- but we can add as much as attributes as we want
- can be created using simple form or JSON view
- there is the power of dynamo db

### primary keys

- primary key should be scalar (only one value and it can be string, binary or number) (example genre is a list not
  scalar)
- uniquely identifies items in a table
- specified in the beginning when creating the table
- required for data organization and retrieval
- types of primary key :
    - partition key
        - (one single hash attribute)
        - items cannot have the same partition key
    - composite key (two keys )
        - know as hash and range attribute
        - contains partition key and sort key
        - item can have the same partition key , but different sort key
- most efficient way to retrieve data
- determines the physical partition where data is stored
- question :
    - what if we want to query data using an attributes => secondary indexes

### secondary indexes

allowing to query data using alternative way than the primary key (performance)
secondary index types :

- local secondary index (LSI)
    - index has the same partition key as the base table but a different sort key,
    - created in the same time as the table and cannot be modified after table creation
    - maximum of 5 local secondary indexes per table
- global secondary index (GSI)
    - an index with a partition key and sort key that can be different from the base table
    - can be modified afterwards
    - maximum of 20 GSI per table
    - be aware of the relationship between the write capacity of GSI and the base table <=> when the write throttle,
      base table writes may throttle too
- how to choose between the two of them :
    - LSI : need to maintain the same partition key but also have to perform some additional sorting or query within the
      same partition
      key, (consistency is important)
    - GSI : more flexibility for various access pattern for fast performance on different attributes
- example of use :
    - for the same product as book, let's say we have to categorize the data based on the author
    - so the author would become the primary key of our GSI and then the book_id would be the sort key
    - so Global Secondary Index is always a composite key
- how to create a secondary key => projecting attributes
    - attributes that are copied from a table to an index
    - attributes to copy can be specified (of course depend on the attributes we want to query on )
    - maximum 20 projected attributes per index
- 3 options of projecting attributes :
    - all : all of the attributes from the base table are projected into the index (performance is important and the
      need to access all attributes because of changing access pattern) (additional storage)
    - keys only : only the key attributes from the base table are projected into the index (cost effective)
    - include option : only specific attributes from the base table are projected into the index (for know access
      pattern)

hands on todo and solve ambiguity on projecting attributes for keys only ? isn't it default since just keys are sent to
index ????

### dynamodb streams

- catch all the changes in our table (delete, update, insert)
- changes are sent to a stream record (one record is one change)
- changes are chronologically ordered
- have to been activated (the stream) (disabled by default)
- real time access
- organized in shard (but fully managed)
- data in the stream is retained 24 hours
- stream record options :
    - Keys_only : view only the key attributes of the item modified
    - New_image : view the item after changes were made
    - Old_image : view the item before changes were made
    - Naw_and_old_image for example for auditing
- use cases :
    - aws lambda
    - amazon kinesis data stream => data firehouse
    - elasticsearch service
    - custom applications
    - aws glue
    - cross-region replication
- use case for lambda hands on : activate dynamo stream > create lambda > configure event source mapping as trigger from
  new
  records
    - records and streams > turn on  > view type (new_and_old)
    - lambda can get access from the stream (iam role)

### APIs

basically for programmatically interact to dynamoDB

- high level operations :
    - control plane (managing dynamodb itself , like creating tables, setting up streams on config some secondary index)
        - CreateTable
        - DescribeTable
        - ListTables
        - UpdateTable
        - DeleteTable
    - data plane directly deal with the data (CRUD)
        - uses PartiQl query language, SQL-like language for dynamoDb
            - ExecuteStatement (reads multiple items from a table, can write or update a single item)
            - BatchExecuteStatement (writes, updates, or reads multiple items from a table)
        - dynamo classic CRUD APIs
            - the primary key must be specified
            - PutItem
            - BatchWriteItem
            - GetItem
            - BatchGetItem retrie up to 100 items from one to more tables
            - Query retrieves all items that have a specific partition key
            - Scan retrieves all items in the specified table or index
            - UpdateItem
            - DeleteItem
            - BatchWriteItem
    - dynamoDB streams APIs to access and manage stream data (enable stream, access stream records or process stream
      data)
        - ListStreams returns list of all streams or a stream for a specific table
        - DescribeStream
        - GetShardIterator to read stream from a specific position
        - GetRecords retrieves one or more stream records using a given shard iterator
    - transaction (manage many operations in a one or nothing operation)
        - transactions provide atomicity, consistency, isolation, durability (acid)
        - can use PartiQl or classic CRUD APIs
            - PartiQl : ExecuteTransaction batch operation that allows CRUD operations on multiple items both within and
              across
              tables
            - DynamoDB Classic CRUD APIs :
                - TransactWriteItems a batch operation that allows Put, Update, and Delete operations on multiple items
                  within and across tables
                - TransactionGetItems : a batch operation that allows Get Operations to retrieve multiple items from one
                  or more tables

### dynamo accelerator (DAX)

dynamoDB in memory cache that improves performance by 10x with microseconds latency (for read actions)
basically for high throughput and low latency for read in dynamodb (by caching frequently access data)

to enable it :

- create a DAX cluster : one or more nodes running on individual instances with one node as primary
- accessing DAX : applications can access DAX through endpoints of the DAX cluster
- throttling exception : if requests exceed the capacity of a node (DAX limits) (may need retries)
- on read operations : checks the cache first, if data in cache (cache hit) => returns directly , if not (cache miss) =>
  DAX forward the request to DynamoDb
    - API calls : Batch/GetItem/Query/Scan
- on write operations : data is writen to the dynamo table and then to the DAX cluster:
    - API calls : BatchWriteItem/UpdateItem/DeleteItem/PutItem

### capacity modes

cost and configuration
read/write capacity modes

on-demand :

- pay per read/write operation without pre-specifying throughput
    - flexibility : ideal for unpredictable or spiky workloads
    - performance : maintains consistent, low-latency performance at any scale (request never throttle)
    - management : handle scaling, reducing operational overhead
    - cost implications : more expensive for predictable workloads (premium for scalability)

provisioned mode :

- specify expected reads/writes per second in RCUs (read capacity units) and WCUs
    - cost efficiency (more economical for predictable workloads)
    - auto-scaling (automatically adjusts throughput based on traffic, optimizing costs)
    - throttling risk (exceeding provisioned throughput can lead to throttling)
    - management overhead : requires monitoring and occasional manual adjustments
- reserved capacity feature (in alignment with the provisioned mode) :
    - long term commitment : commit to specific RCUs and WCUs for 1 or 3 years
    - discounted pricing (reduced rates)
    - use case: suited for stable, predictable workloads over long periods
- autoscaling in combination with provisioned mode too :
    - dynamic scaling : adjusts throughput based on utilization
    - cost optimization : lowers costs by matching capacity to demand
    - setup complexity : requires setting minimum , maximum and target utilization levels
    - response time : minor delays in scaling might occur, but it's designed to be responsive
    - might be subject to throttling

hands on : unit of capacity mode can be updated

- how to update : table > action > update settings > edit (can be changed even if the table is already created)
- also possible to check the option use the same capacity settings for all global secondary indexes (they also have a
  dedicated capacity in general)
- example provisioned RCU 2 , autoscaling 1 to 10 , target 70 % , will be reduced to 1 since no read action made

### WCU and RCU

write / read capacity unit
measures write / read throughput

- WCU write capacity Unit
    - definition : 1 WCU equals to 1 write per seconds for items up to 1KB
        - consumption : items over 1KB require more WCUs : e.g. 3KB item needs 3WCUs per write
    - provisioning :
        - allocate WCUs based on expected writes
        - adjust with over-provisioning for spikes or use auto scaling for dynamism
        - cost : pay for provisioned WCUs, used or not, planning is important to manage expenses
    - throttling :
        - exceeding WCUs leads to throttled writes, potentially causing ProvisionedThroughputExceededExceptions
        - opt for on-demand capacity for automatic scaling
- RCU quite similar
    - definition : 1 strongly consistent read per second or two eventually consistent reads per second for items up to
      4KB
    - read types :
        - eventually consistent reads : fast, high throughput, but data might be slightly outdated
        - strongly consistent reads : ensures the latest data view at a higher cost
            - guaranteed that a read will reflect all of the writes that were successful before the read was initiated
            - may impact the performance, little higher latency,
        - e.g. total data 1 item 8 KB
            - for eventually consistent reads needs 1 RCU
            - for strongly consistent read unit need 2 RCUs
        - e.g.2 10 items 3KB each
            - for eventually consistent reads need 5 RCUs for 10 with strongly consistent
- throughput calculation (hands on) : larger items consume more WRUs/RCUs
    - on creating new table > custom settings > provisioned mode > there is a capacity calculator
- pricing :
    - on demand : each request up to 1KB
        - standard table pay per request $1.25 per million write request units / $0.25 per million for read
        - infrequent access $1.56 per million write request units / $0.30 per million for read
    - provisioned : each item up to 4KB
        - standard table $0.00065 per WCU / $0.0001 per RCU
        - infrequent access $0.00081 per WCU and $0.00016 per RCU

### hot partitions and throttling

hot partition :

- overloaded partitions due to uneven data distribution
- caused by poorly chosen partition keys

throttling

- throttling : happens when requests exceed table/index throughput limits

solution :

- even data distribution : use well-designed partition keys
- exponential backoff : incorporate into retry logic (wait a little bit longer)
- monitor throughput : use cloudwatch, adjust settings as needed
- use DAX : cache reads to reduce table load for frequently accessed data

performance optimization

- burst capacity : dynamodb provides a burst capacity means this allows table to accommodate short peaks of read or
  write capacity without throttling
    - allows handling short traffic spikes
    - uses saved unused capacity for up to 5 minutes (accumulated to the actual throughput)
- adaptive capacity
    - automatically balances throughput across partitions where access pattern is not so even (equitable)

### time to live

feature that can be enabled to automatically delete items in a table by setting an expiration date

- expired items are deleted 48 hours after the expiration date
- ttl does not consume write throughput
- expired items pending deletion can still be updated (ttl attribute can be removed)
- expiration timestamp should be in unix epoch format (time since january 1st 1970)
- deleted items appear in dynamodb streams as service deletion
- hands on :
    - it is set by adding a new attribute (type number) with the value of expiration date in epoch format (website epoch
      converter)
    - under table details > additional settings > TTL > turn on > specify the attribute > once the value is exceeded
      data will be automatically deleted > run preview

[<<Home page](./../README.MD#dynamodb)