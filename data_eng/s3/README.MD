<a id="s3"></a>

# s3

### partitioning

Partitioning refer to the way folders are structured, it can be time-based, location-based, ...

- benefits :
    - data management :
        - can apply some rules based on partitioned data (example lifecycle)
    - performance increase :
        - improve the performance of athena queries since requests are filtered only on relevant data
        - reducing the data being scanned leading to cost savings
- how to :
    - organize data into folders and subfolders including the use fo buckets
    - use glue crawlers to automatically create partition keys
- common example :
    - time-based partitioning :
        - 2021/month=11/day=05/filename.txt
    - introduction of metadata tagging for custom metadata attachment ?????
- hands-on :
    - organizing data based on location :
        - create bucket and folder london bucket/london
        - create folder new york bucket/new_york
        - upload london data to london folder and do the same for new_york
        - create crawler :
            - data source select the bucket
            - select role
            - run the crawler
        - see the table would be created and column partition key is created too (partition_0)
        - now if we run a query filtered using partition, data scanned is less than filtering using the column location
    - add files on existing partition would have any problem
    - adding new partition need little manoeuvre :
        - create folder tokyo bucket/tokyo
        - upload tokyo files
        - running query would not make new data appear on athena
        - little work around to do : 2 ways to do it :
            - manually :
                - create folder tokyo and upload file (note while executing athena query data is not collected)
                - execute query :
              ```sql
                  ALTER TABLE mytable
                  ADD PARTITION (partition_0='tokyo') 
                  LOCATION 's3://mybucket/tokyo/'
              ```
            - automatically : execute the following query :
              ```sql
                  MSCK REPAIR TABLE mytable
              ```

### storage classes

- Choosing the right storage class based on frequency of access
- Default is STANDARD storage class, we might send to archival or even delete data
- Different storage classes :
    - S3 Standard : default, frequent access, low latency and high throughput
        - uses cases : cloud/mobile and gaming applications, dynamic websites, content distribution, big data analytics
    - S3 Intelligent-Tiering : best for unknown or changing access patterns (automatically moves data to the most
      cost-effective access tier):
        - frequent access tier
        - infrequent access tier (example moved if data is not accessed in 30 consecutive days)
        - archive instant access tier (example moved if data is not accessed in 90 consecutive days)
        - Optional Asynchronous Archive Access Tier
            - Archive access tier
            - deep archive access tier
    - Amazon S3 Express One Zone :
        - high performance, can improve data access by 10x
        - single availability zone
        - reduce request costs by 50% compared to S3 Standard
        - data is stored in different bucket type (Amazon S3 directory bucket which supports 100000 requests/second)
    - S3 Standard-Infrequent Access
        - access less frequently, but requires rapid access when needed
        - used for long lived data but infrequently accessed
    - S3 One Zone-Infrequent Access almost the same as S3 Standard-Infrequent Access but one availability zone only
        - ideally for storing secondary backup of on-premises data
    - S3 Glacier Instant Retrieval
        - long live
        - access once a quarter
        - used for data that needed to be accessed once a quarter and with instant retrieval in milliseconds
    - S3 Glacier Flexible Retrieval
        - access once on 2 times a year
        - restoration time varies from a minute to 12 hours
        - used for long-term backups and archives with retrieval option
        - configurable retrieval times from minutes to hours with free bulk retrievals
    - S3 Glacier Deep Archive
        - is the cheapest option
        - long-term archival of data with access once or twice a year
        - objects can be retrieved within 12 hours (with restoration fees)

- pricing (example us east)

  | Storage class                                    | use case                                                                          | pricing                                                 |
                                                                                                                                                                                                                                                            |--------------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------|
  | S3 Standard                                      | General purpose / frequently accessed                                             | 0.023/GB                                                |
  | S3 Standard - Infrequent Access                  | long lived but infrequent access, need millisecond access                         | 0.0125/GB                                               |
  | S3 One Zone - Infrequent Access                  | re-creatable infrequently, need millisecond access                                | 0.01/GB                                                 |
  | S3 Intelligent tiering                           | Automatic cost savings, unknown or changing access patterns                       | frequent access : 0.023/G, infrequent access : 0.0125/G |
  | S3 Intelligent tiering Asynchronous Access Tiers | asynchronous archive access tiers                                                 | archive access 0.0036/G , deep archive 0.00099/G        |
  | S3 Express One Zone                              | high performance storage for most frequently accessed data                        | 0.16/GB                                                 |
  | S3 Glacier Instant retrieval                     | long lived archive data, access once a quarter, instant retrieval in milliseconds | 0.004/GB                                                |
  | S3 Glacier Flexible retrieval                    | long-term backups and archives with retrieval option from 1 minute to 12 hours    | 0.0036/GB                                               |
  | S3 Glacier Deep Archive                          | long-term archive, access once or twice a year, retrieve within 12 hours          | 0.00099/GB                                              |

### lifecycle rules

set of rules that define actions to be applied to a group of objects inside s3 bucket

- transition actions (example after 30 days, we made transition to cheapest storage class)
- expiration actions
- lifecycle rules are under management of the bucket

### versioning

manage changes in files by keeping multiple versions
revert back to previous states in case of accidental deletion (part of disaster recovery strategy)
versions are immutable (integrity)

challenges :

- increase storage needs
- not incremental versioning
- complexity in managing multiple versions

balancing act:

- need to find balance between benefits and additional storage costs
- data lifecycle policies help define retention periods for previous versions

implementation :

- just enable versioning for s3 buckets (bucket > properties > versioning ???)
- s3 keeps multiple version of an object
- building strategy :
    - not necessary to enable versioning for all data
    - enable for critical or sensitive datasets
- documentation :
    - should maintain clear doc of versioning strategy
    - document which data is versioned and why

Note :

- Versioning might affect lifecycle rules
- if versioning is activated, a delete object would just put a delete marker on the object (not permanent)

### Replication (cross region replication)

we have 2 buckets A (original) from region us-east-1 and B eu-central-1 (copy synchron of A)

benefits :

- disaster recovery :
    - safeguarding data in case of outages or disruptions
    - additional redundancy ensuring data availability
- latency reduction :
    - reducing data access times for users in different regions
    - improving user experience by placing data closer to users

additional costs :

- cross region replication comes with additional cost
- additional data transfer costs when moving data across regions

when to use ? if availability of data is critical or if latency is very important but have to balance with those costs

implementation in AWS :

- replication rules and policies (to set in the source bucket)
- automated replication of new objects added to the source based on configuration rules
- direction of replication (only one direction source -> to replication)
- versioning needs to be enable in both source and destination
- how to implement :
    - on source bucket > go to management > under replication rules > create replication rule
    - replication rules can be filtered under scope/prefix ...
    - then browse to the target bucket
    - should add an IAM role
    - can enable replication time control (RTC), will increase the replication time but additional fees
    - can active on not the replication of already existing objects
    - activate or not replication of deletion

### s3 security

encryption : in transit or at rest

- in transit encryption, AWS uses TLS (transport layer security) or SSL (secure socket layer)
    - would encrypt on the client side, then transport it securely to s3, then decrypts it there, then s3 encrypt
      again (if configured to do so)
- at rest : data is encrypted and then stored as it is, can be done at server side or client site
- all buckets always have activated the encryption at rest as default
- encrypt data at rest then decrypt it on download

- different method of encryption :
    - server-side encryption with amazon s3 managed keys (SSE-S3) (default configuration) (amazon managed key)
    - server-side encryption with AWS KMS (SSE-KMS) (using KMS managed key, KMS can be created by ourselves, we can also
      manage a policy such as who can use the key)
    - dual layers server-side encryption with AWS KMS keys (DSSE-KMS), data is encrypted twice, each time use different
      KMS key
    - server-side encryption with customer-provide keys (SSE-C) (we must provide our own key), and when upload a file,
      we have to send the encryption key as param to the API, we are responsible of securing the keys in transit and at
      rest, and regularly rotate
- how to :
    - while creating the bucket, section default encryption
    - while uploading objects, encryption can be override, or after the upload (under properties of the object)

### bucket policies

set of rules which specify who can access the objects inside our bucket and what action they can perform
example :

```json
{
    "version":"2012-10-17",
    "Statement": [
        {
            "Effect":"Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::yourbucketname/*",
            "Condition": {
                "IpAddress":{
                    "aws:SourceIp":"19.168.100.0/24"
                },
                "Bool":{
                    "aws:SecureTransport":"true"
                }
            }
        }
    
    ]
}

```

principal : who ?

### access points

problem : many users/apps can access the data inside bucket
solution : create access points with specific entry points that define who can access which data and how without the
needs to update structure of data inside the bucket
each access point :

- its own DNS name (internet access VPC access)
- access point policy (i.e. bucket policy)
- features : customized permissions, improved scalability and organization, enhanced security

### object lambda

s3 feature which allows to transform data as it is retrieved from s3 (modify data on the fly) without the need to
duplicate data
e.g :

- filter out sensitive information (staring password for example)
- transform data format (csv -> json)
- aggregate data (join from another services for example)
- backed by object lambda access point, lambda access point is connected to a lambda function,
    - the lambda function can access data directly on s3 or through s3 access point

### s3 event notification

- every action to a s3 bucket is subject to a notification
    - e.g : a file upload will result a s3:ObjectCreated:Put notification (action s3:PutObject)
    - it can be restoring object, deleting object ...
    - lifecycle expiration events, lifecycle transition events, intelligent tiering automatic archival events, ...
    - object tagging or even object ACL put events
    - we can also use wildcards as s3:ObjectCreated:* to list all creation (Put, Post, ...)
- with such event we can trigger a lambda for example, send to sqs, sns, route to EventBridge
- we can filter events too :
    - prefix filter : IMAGES/ will send an event on every action inside the folder IMAGES/
    - suffix filtering : 'jpg' (only image files)
- hands-on : notification of object creation and send to sns topic:
    - creating sns topic, use bucket arn to allow the principal to publish notifications to the topic
    - on s3 bucket > properties > event notifications > create a notification > choose sns and select the topic
    - subscribe to the topic : under subscription > create subscription > add email address > then confirm
      subscription (sent to the email)

### data mesh

- definition : architectural concept or set of guiding principles and best practices for decentralized data management
  (ownership)
- goal :
    - improve data quality
    - improve scalability of data governance
- how it works : it treats data as a product and assigns domain oriented responsibilities
    - each domain of an organization owns its data (product) and also responsible for its governance (quality and
      accessibility)
    - e.g. marketing and sales department, they own their data as product and responsible
- example of services to achieve that goal :
    - s3 (scalable storage)
    - glue (for data cataloging and ETL process)
    - redshift (data warehousing and analytics)
    - aws lakeformation (data lake security and governance and general datalake setup)
    - athena for serverless querying
    - api gateway for exposing data products as APIs
- data mesh principles :
    - distributed domain-driven architecture (data ownership is assigned to the domains that understand the data best)
    - data as a product (focus on quality, discoverability, and usability)
    - self-serve data infrastructure (all business units process and store their data products)
    - federated data governance (ensure the compliance and security across the organization while still allowing
      autonomy of standards and policy implementation within the domain)

### data exchange

centralized data catalog which allows customers to securely find, subscribe to and use third party data in the cloud

- use cases :
    - financial services data
    - healthcare
    - geospatial analysis
    - retail and consumer insights (trends or customer behavior)
- available solution :
    - data sets can be publish on aws marketplace (provider should be registered as sellers)
    - data exchange also support aws lakeformation data permissions
        - this allows subscribers to access the data stored in a providers lake formation data lake
    - s3 : data providers can import and store data files in their s3 buckets, and subscribers can export those files to
      their own s3 buckets

[<<Home page](./../README.MD#s3)