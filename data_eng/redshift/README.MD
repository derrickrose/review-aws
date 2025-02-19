# redshift datawarehouse

### overview

- fully managed, highly available, cost-effective petabyte-scale data warehouse service
- ANSI SQL compatible relational database
- can be accessed using amazon redshift query editor v2 or any other BI tools
- support loading multiple data formats, including : csv, json, apache parquet, ORC
- cluster architecture and easily resizable as the data is growing
- stores data in columnar format (not like Online Transactional Processing OLTP databases) for performance purposes
- uses massively parallel processing (MPP) also very important for read performance (in a distributed way)
- integration with other aws services s3, lambda, glue, dynamodb ..
- advanced compression (reduce storage)
- security features (encryption at rest, in transit, acl, iam role, vpc, security groups ...)
- use cases : data warehousing, BI, analytics, log analysis, iot data processing, real-time dashboard

### architecture : cluster and nodes

amazon redshift cluster

- core infra component of redshift
- runs on amazon redshift engine and contains one or more databases
- executes workloads coming from external data apps
- uses replication and continuous backups (availability and durability of data)
- automatically recovers from failures (if component is failing, automatically replaced)
- composed with 2 components :
    - leader node communicating with the client (ODBC or JDBC)
        - is always provisioned and coordinates two or more compute nodes
        - aggregates results from compute nodes before sending the results
        - develops execution plan (series of step taken by compute nodes)
        - compiling the code and distributing it to compute nodes then assigns a portion of the data to each compute
          node
        - redshift is designed such certain SQL queries are only executable on the leader node
    - compute nodes (storing data and execute the queries as instructed by the leader node)
        - has their own CPU, memory, disk storage
        - run the query execution plans
        - transmit data among themselves
        - capacity can be increased by increasing the number of nodes, upgrading the node type or both
- use provisioned cluster or redshift serverless
- create redshift cluster (hands on) :
    - create cluster > name > choose node type > choose number or nodes > active checkbox load sample data > database
      configuration > admin user > password > iam role > create role > additional configurations > vpc > database name >
      database port > encryption > monitoring > backup > cross region > create cluster

### access redshift cluster (hands on)

- accessing redshift cluster can be done using :
    - the aws console
    - aws cli
    - using own sql client by downloading te jdbc or odbc driver, copy the connection url (endpoint, jdbc/odbc url)
- how to access :
    - redshift landing page > cluster > query data
- access options :
    - database user and password
    - federated user
    - temporary credentials using database user
    - temporary credentials using iam
    - aws secrets manager
- on the console we able to see some metrics :
    - capacity usage
    - CPU utilization
    - snapshot
- note we can pause the cluster

### node types and storage

redshift managed storage (RMS)

- uses large high performance solid state drives (SSDs) for fast local storage
- uses s3 for longer-term durable storage (if data is growing, it offload the data in s3):
    - => hot blocks are stored in local and the cold blocks (infrequently used data) are stored in s3
- pricing is the same for RMS regardless of whether the data resides in high-performance SSDs or in s3
- 2 types of nodes :
    - RA3 :
        - uses redshift manage storage (RMS)
        - separates compute and storage
        - supports multiple availability zone
    - DC2 :
        - local SSD storage included
        - stores data locally for high performance
        - available on single availability zone (AZ) only
        - not decoupled
        - recommended by AWS for datasets under 1TB (compressed)

### Resizing methods

sometimes we need to modify the number of nodes or the type
node slices :

- compute nodes are split into slices
- each handling a part of the workload
- leader node distributes data and tasks to the slices for parallel processing

- elastic resizing:
    - allows to update the number of node or update node type (e.g. from DS2 to large DC extra large)
    - this is done without any downtime
    - completes quickly (about 10 minutes)
    - during the resize, some queries can complete successfully, but others can be dropped
    - on running this kind of operation, a snapshot will be created and data is redistributed from the source cluster
      and the cluster that is compromised of the new node type (running query will be dropped but it recover quickly )
    - we cannot un-definitely add node, there is limitation for elastic resizing

- classic resizing
    - takes more time
    - to be used when it is not anymore possible to use elastic resizing due to limitation of the elastic resizing, or
      the type of nodes is not supported

### snapshots and sharing

snapshots : point in time backups of a cluster
snapshots are stored internally on s3 (use encrypted connection for the transfer to s3 SSL)
snapshot can be taken manually or automatically

- automated snapshot (incremental snapshots are taken automatically) enabled by default :
    - every 5 GB per node of data changes
    - every eight hours
    - note : if the 5 GB come first, there still a minimum time between the snapshots (15 minutes)
    - default retention period is one day

- manual snapshot :
    - can be taken any time
    - by default , manual snapshots are retained indefinitely
    - you can specify the retention period when you create a manual snapshot or you can change the retention period by
      modifying the snapshot
- can share data across aws regions
    - do not have to load snapshot to s3 (it can be done automatically by sharing data)
    - sharing can be done without amazon s3 as a medium
- resizing and snapshots (hands on)

### distribution keys and styles

- cluster store data across compute nodes
- uses distribution keys for that distribution
- distribution styles determine where data is actually stored (which compute node)
- distribute the workload uniformly among the nodes in the cluster
- minimize data movement during query execution

from that comes distribution styles (3 kinds)

- Key distribution :
    - rows are distributed according to the values in one column
    - the leader node places matching values on the same node slice
    - useful for tables that participate frequently in joins
- All distribution :
    - create copy of the entire table and is distributed to every node
    - multiplies the storage required by the number of nodes in the cluster
    - is appropriate only for relatively small and slowly changing tables
    - faster query operations
- Even distribution :
    - leader node distributes the rows across the slices (regardless of the values in any particular column)
        - when we don't know exactly that there is an obvious key column to distribute data by
    - appropriate when a table doesn't participate in joins
    - appropriate when there isn't a clear choice between key distribution and all distribution
- Auto distribution (default value):
    - redshift assigns an optimal distribution style based on the size of the table data
        - sometimes need to reconfigure ourselves because we saw that tables causing a lot of workload
    - when the table is small style is set as default, then when the data is much larger, redshift may change it to key
      then if it goes larger again it will change to even
    - the change in distribution style occurs in the background with minimum impact to the user queries

### redshift vacuum

because over time as we add or delete and update rows, data can become fragmented (increase storage usage and query
performance), so vacuum is here used to :

- re-sorts rows and reclaims disk space (specific table or all tables)
    - since when we delete data, disk space used is not immediately freed up, it is just marked as available to reuse
    - and therefore we have this vacuum command to really clean disk
- redshift automatically sorts data and runs VACUUM DELETE in the background
- redshift automatically performs a DELETE ONLY vacuum in the background
- vacuum command can be run manually
- vacuum will skip sorting for tables where above 95 percent are already sorted (this threshold can be set, but default
  is 95)
- users can access tables while they are being vacuumed (even if they are blocked for updates or deletes )

command syntax :

VACUUM [FULL|SORT ONLY|DELETE ONLY|REINDEX|RECLUSTER] [[table_name][ TO threshold PERCENT] [BOOST]]

- FULL sorts the specified table and reclaims disk space (default)
- SORT ONLY sorts the specified table (or all tables) without reclaiming space
- DELETE ONLY reclaims disk space only (temporarily lock the update and delete)
- REINDEX rebuilds the indexes on the tables (useful for tables using interleaved sort keys multiple column as sort key)
- RECLUSTER sorts the portions of the table that are unsorted (recommended for table with frequent ingestions)
- TO threshold PERCENT specifies a threshold above which VACUUM skips sort phase and reclaiming space in delete phase
- BOOST runs the vacuum command with additional resources as they are available

### redshift integrations

- s3 :
    - copy command to copy data from s3 to redshift
    - unload to export data from redshift to s3
    - redshift spectrum which allows redshift to query data stored on s3

- emr :
    - load from emr to redshift
- lambda
    - invoke lambda function from redshift (within a query )
- dms : as a target of data migration
- ec2 : load data from ec2
- data pipeline : perform some transformation from in and out to redshift using data pipeline
- stream into materialized view (lowering the time to access data and cost of storage):
    - kinesis streams
    - managed streaming for apache kafka
- dynamodb table

COPY command

- is used to load large amount of data from outside of redshift
- it uses MPP (massive parallel processing)
- e.g.: copy favoritemovies from 'dynamodb://movies' iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
- uses optimal compression scheme :
    - gzip, izop, bzip,
- decrypts data as it is loaded from s3
- COPY or INSERT but COPY is faster

Moving data between s3 to redshift

- redshift auto copy from amazon s3
- enhanced VPC routing (enables to route the network traffic through a VPC instead of the internet)

Amazon Aurora zero-ETL integration

- allows changes made to the amazon aurora RDBMS database to be replicated in the amazon redshift database seconds after
  the aurora updates
- eliminates the need for custom data pipelines

Load data from S3 hands on
do not forget to create table
can be done using command on redshift editor v2 or with visual interface of the console

```sql
COPY yourtable  -- public.orders for example with public schema and table orders
FROM 's3://your-bucket-name/your-folder-name/'
CREDENTIALS 'aws_iam_role=arn:aws:iam::your-account-id:role/your-role-name'
DELIMITER ','
IGNOREHEADER 1
REGION 'us-east-1'
```

### export data from redshift to s3 (hands on)

UNLOAD command

- allows to export the results of a query to amazon s3
- it supports exporting data in various formats (csv, parquet, orc, ...)

```shell
UNLOAD (SELECT * FROM yourtable)
TO 's3://your-bucket-name/your-folder-name/' -- we can specify a file name when PARALLEL is OFF
CREDENTIALS 'aws_iam_role=arn:aws:iam::your-account-id:role/your-role-name'
DELIMITER AS ','
ALLOWOVERWRITE
PARALLEL OFF;
```

### transformation with ELT (data transformation using Amazon Redshift)

- Design patterns when moving data from source systems to a data warehouse

    - ETL : Extract Transform Load
    - ELT : Extract Load Transform

- Amazon redshift provides a functionality to process all your data in one place with its in-database transformation (
  ELT)
  capabilities

    - sql transformation
    - stored procedures
    - user-defined functions (UDFs)

- Amazon redshift can connect to an ETL platform of using JDBC or ODBC
- popular ETL platforms that integrate with Amazon Redshift include third-party tools like :
    - Informatica
    - Matillion
    - dbt
    - AWS-native tools like AWS Glue

### federated queries (query data outside of redshift)

- traditionally we load data from all different sources into redshift then perform our analytical queries
    - problem :  resources intensive, need planning to move all data ...
- this feature allows us to combine and analyze data across different data sources
    - => specially and only for relational databases
- reduces data transmission while optimizing efficiency
- eliminates the necessity of ETL pipelines
- so this needs to be compatible with PostgresSQL (because redshift is designed in this way)
- so we can include Amazon RDS for PostgresSQL (for example) => query data onlive from RDS
- also Amazon Aurora
- other data source on-premise accessible via JDBC

- uses external schema definition
- can be used to incorporate live data
- distributes part of the computation for federated queries directly into the remote databases (minimum data
  transmission)
- uses parallel processing

### materialized views

- contains a precomputed result set
- if data in table have changed, view should be updated too
- can issue a SELECT statement to query it
- redshift returns the precomputed results from the materialized view

- query results are returned much faster (than a complex query)
- useful for speeding up queries that are predictable and repeated
- can create a materialized view from another materialized view as reference
    ```sql
    CREATE MATERIALIZES VIEW myview
    AUTO REFRESH {YES|NO}
    AS query
    ```

- feature very important is to use materialized view for Streaming Ingestion (kinesis data stream or managed streaming
  for apache kafka ...)
- steps for creating a streaming ingestion :
    - create an external schema that maps to the streaming data source
      ```sql
      CREATE EXTERNAL SCHEMA evdata FROM KINESIS
      IAM_ROLE 'arn:aws:iam::0123456789:role/redshift-streaming-role';
      ```
    - create a materialized view to consume the data
- updating materialized view
    - automatic refresh option to refresh materialized views when base tables of materialized views are updated
    - auto refresh operation runs at at time when cluster resources are available to minimize disruptions to other
      workloads
    - specify auto refresh in the materialized view definition to enable it
    - schedule it using Scheduler API and console integration
    - manually refresh any materialized views using the REFRESH MATERIALIZED VIEW statement from query editor v2
- as summary :
    - create materialized view
    - alter materialized view
    - refresh materialized view
    - drop materialized view

### federated queries and materialized views (hands on)

- create external schema first
    ```sql
        CREATE EXTERNAL SCHEMA myschema 
        FROM POSTGRES DATABASE 'mydatabase' SCHEMA 'public'
        URI 'my-instance-endpoint'
        IAM_ROLE 'arn:aws:iam::0123456789:role/redshift-federated-query-role'
        SECRET_ARN 'arn:aws:secretsmanager:region:0123456789:secret/secret-name'; --database credentials
    ```  
- create materialized views as show on previous lesson

### amazon redshift spectrum

- used to query data stored in s3 buckets
- how to ?
    - define external tables in redshift cluster that reference the data files stored in s3 (external data catalog)
    - the external tables just define the structure of those data but they are still reside in s3 (no transmission)
- supports different data formats , gzip and snappy compression
- resides on dedicated amazon redshift servers (independent of the cluster)
- also many of the compute-intensive tasks are pushed to redshift spectrum layer so that the queries require less of the
  cluster capacity
- scales intelligently
- the external data catalog can be :
    - aws glue
    - amazon athena
    - apache hive metastore
- change made on the external data are directly updated on the redshift cluster
- you can partition the external tables on one or more columns
- redshift spectrum tables can be queried and joined just as any other amazon redshift table
- amazon redshift spectrum considerations :
    - redshift cluster and the s3 bucket must be in the same aws region
    - redshift spectrum doesnt support enhanced VPC routing with provisioned clusters > need to set additional
      configurations
    - supports amazon s3 access point aliases
    - redshift spectrum doesnt support vpc with amazon s3 access point aliases
    - cant perform update or delete operations on external tables
    - to create a new external table in the specified schema, you can use CREATE EXTERNAL TABLE
    - to insert the results of a SELECT query into existing tables on external catalogs, you can use INSERT (external
      table)
    - unless you are using an AWS Data Catalog that is enabled for AWS Lake Formation, you cant control user permissions
      on an external table
    - to run spectrum queries, the database user must have permission to create temporary tables in the database
    - redshift spectrum doesnt support amazon EMR with kerberos
- hands on
    - create external schema (data catalog on glue)
        ```
          CREATE EXTERNAL SCHEMA spectrum_schema
          FROM DATA CATALOG DATABASE 'spectrum_db' IAM_ROLE 'arn:aws:iam::012345678910:role/your-role'
          CREATE EXTERNAL DATABASE IN NOT EXISTS;
        ```
    - create external table
        ```
            CREATE EXTERNAL TABLE spectrum_schema.orders (
                order_id VARCHAR(20),
                order_date DATE, 
                customer_name VARCHAR(100),
                ...
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            LOCATION 's3://yourbucket/your-folder';
        ```
    - should be visible in glue

### system table views

- system table: contain information about how the system is functioning (useful for administrative tasks)
    - example : we can see system table to see what are the running queries
    - we might also use some of those views or tables for improving query performance
    - basically used to gain information and also just to monitor the health and help improve performance or queries or
      cluster
    - can be queried like other normal database tables, but not necessarily have access to all the tables (some are used
      by aws staff for diagnostic purposes)
    - and also some of them are only visible to super users and some of them are visible to all the users
- types of system tables and views
    - SVV views :
        - details on database objects
        - SVV_ALL_TABLES see all tables (also external tables)
        - SVV_ALL_COLUMNS see a union of columns
    - SYS views :
        - monitor query and workload performance in clusters
        - SYS_QUERY_HISTORY : see details of user queries
    - STL views :
        - generated from system logs for historical records
        - STL_ALERT_EVENT_LOG identify opportunities to improve query performance basically coming from query optimizer
        - STL_VACUUM statistics for tables that have been vacuumed
    - STV tables :
        - snapshots of the current system data
        - STV_EXEC_STATE : information about queries an query steps actively running
    - SVCS views
        - details about queries on both the main and concurrency scaling clusters
        - SVCS_QUERY_SUMMARY : general information about the execution of a query (most likely the same as
          SYS_QUERY_HISTORY)
    - SVL views
        - contain references to STL tables and logs for more detailed information
        - SVL_USER_INFO data about amazon redshift database user

### redshift data API

- it is a lightweight, http based API that is used for running queries against Amazon Redshift (no need to use
  persistent
  db connection)
  e.g. :
    - aws lambda
    - sagemaker notebooks
    - other web-based applications
- can be used to run SQL queries asynchronously
- can be used as an alternative to using JDBC and ODBC drivers
- can be set up with very little operational overhead (very easy to set up)
- to take in consideration  :
    - maximum duration of a query is 24 hours
    - maximum number of active queries per amazon redshift cluster is 200
    - maximum query result size (after compression is 100 MB)
    - maximum retention time for query results is 24 hours
    - maximum query statement size is 100 KB
    - is available to query single node and multiple node clusters of the following node types :
        - dc2.large, dc2.8xlarge, ra3.xlplus, ra3.4xlarge, ra3.16xlarge
- access control : authorize user/service by adding managed policy (AmazonRedshiftDataFullAccess)
- monitoring data API : can be monitored in aws EventBridge
    - eventbridge then routes data to targets such aws lambda or sns
- option to schedule data api call operations within eventbridge

### redshift data sharing

- used to securely share access to live data across different clusters/workgroups/aws accounts/aws regions/availability
  zones/ (no need to copy data)
    - producer cluster (creating data share, basically database objects) called outbound share
    - consumer cluster (inbound share)
    - each data share is always associated with a specific database
        - and we can add datashare objects (objects from this database that is shared or that is associated with this
          share) tables, views, UDFs, ...
- 3 differents type of share :
    - standard datashares
        - can share data across clusters and also serverless workgroup's availability zones accounts and regions
    - aws data exchange datashare
        - licensed data sharing via data exchange and aws is handling the billing and the payments
        - approved providers that can add data shares to products
    - aws managed Lake Formation managed datashare
        - using Lake Formation : centrally define and enforce the database table, column and row level access
          permissions
- important things to take into consideration :
    - consumer is charged for all compute and cross-region data transfer fees
    - producer charged for the storage
    - performance depends on the compute capacity of the consumer cluster
- few limitations when working with the data shares
    - supported for all provisioned ra3 cluster types and amazon redshift serverless
    - for cross-account and cross-region data sharing, both the producer and consumer clusters and serverless namespaces
      must be encrypted (not required to use the same encryption key)
    - you can only share SQL UDFs through datashares, python and lambda UDFs are not supported
    - adding external schemas, tables, or late-binding views on external tables to datashares is not supported
    - consumers cant add datashare objects to another datashare

### redshift workload management (WLM)

- this is a feature that helps with managing the query performance based on priorities
- define how resources are allocated to different queries
    - uses query queues
        - route queries to the appropriate queue
- enables users to flexibly manage priorities within workloads
- can create up to 8 queues

how it works

- automatic workload management
    - redshift manages :
        - how many queries run concurrently
        - how much memory is allocated to each dispatched query
    - when complex queries => lower concurrency
    - when lighter queries => higher concurrency
    - you can configure the following for each query queue :
        - queue : configurable with different priorities and rules
        - user groups : assign a set of user groups to aqueue (if those users are running query, query are sent to
          specific queue)
        - query groups : assign a set to query groups to a queue
        - priority : relative importance of queries (e.g. prioritize etl rather analytical queries)
        - concurrency scaling mode automatically adds additional cluster capacity (available also for manual mode)
- manual workload management (WLM)
    - manage system performance by modifying WLM configuration
    - can configure the amount of memory allocated to each queue

automatic => usually higher throughput (default)
manual => offers more control

### short query acceleration (SQA) (feature of WLM)

- prioritizes selected short-running queries over long-running queries
- uses machine learning to predict the execution time of a query
- runs short-running queries in a dedicated space (no need to wait until long-running queries are finished)
- CREATE TABLE AS (CTAS) statements and read-only queries, such as SELECT statements are eligible for SQA
- this feature is enabled by default

### serverless

different from provisioned :

- no cluster management
- automatic scaling (up or down)
- pay as you go
- automatically provisions and manages capacity for you (different from provisioned you have to build a cluster of node
  type that meet your capacity i.e. capacity, number of node, storage, ...)
- automatically manages resources efficiently and scales based on workloads, within the thresholds of cost control (
  different from provisioned, you have to enable the concurrency scaling on the cluster to face to periods of heavy
  load )
- can choose port between 5431 and 5455 (different from provisioned any port to connect)
- not applicable for resizing (different from provisioned can add or remove node)
- always encrypt data (KMS, or AWS managed or customer managed ) ; actually almost the same for provisioned just in
  provisioned data can be not encrypted

### redshift ml

- allows users to create, train, deploy and apply machine learning models using just SQL with data stored in redshift
- CREATE MODEL command
- lets users to create predictions without the need to move data out of amazon redshift
- useful for users that doesnt have expertise in machine learning, tools, languages, algorithms, and APIs
- redshift ML supports common machine learning algorithms and tasks such as :
    - binary classification, multiclass classification, regression,
- automatically finds the best model using amazon sagemaker autopilot
- under the hood, sagemaker neon is compiling the trained model and makes it available for prediction in the redshift
  cluster => and then when you use the trained model to make predictions, this means you run a machine learning
  inference query, and the query can use the massively processing capabilities of amazon redshift and the query can use
  the machine learning based predictions

### security

provides :

- sign-in credentials
- access management using IAM
- Virtual Private Cloud
- cluster encryption (KMS or own key)
- cluster security groups :
    - default lockdown : when you provision an amazon redshift cluster, it is locked down by default so nobody has
      access to it
    - inbound access control : to grant other users inbound access to an amazon redshift cluster, you associate the
      cluster with a security group (works like a firewall controlling inbound and outbound from specific IP
      address ...)
    - ssl connections to secure data in transit
    - load data encryption : encrypt data during the load process :
        - server side encryption (amazon s3 will decrypt)
        - client side encryption (copy command will decrypt)
- for data in transit is secured
- column level access control
- row level access control

### access control

- you can either manage your users and groups within redshift (authorization on what we can do within the database)
- AWS IAM users (authentication users when they connect to redshift cluster)
- the privileges to access specific objects are tightly coupled with the db engine itself (sql)
- how to ?
    - create users and groups within redshift
        ```sql
        CREATE GROUP human_resource;
        CREATE SCHEMA human_resouerce;
        GRANT USAGE on SCHEMA human_resource TO GROUP human_resource;
        GRANT SELECT ON ALL TABLES IN SCHEMA human_resource TO GROUP human_resource;
        CREATE USER human1 PASSWORD 'abc';
        ALTER GROUP human_resource ADD USER human1;
        ```
    - now what is the difference with role ? since 2022 role base access control in redshift (rbac)
        - work very similarly to groups, assign permissions to the role, then grant this role to the user (or another
          role)
        - note: group cannot contain another group
        - when using rbac, role can give permissions to another role
        ```sql
        CREATE ROLE human_resource;
        GRANT ROLE human_resource TO user1;
        GRANT USAGE on SCHEMA human_resource TO ROLE human_resource;
        GRANT SELECT ON ALL TABLES IN SCHEMA operation TO ROLE finance;
        GRANT ROLE finance TO ROLE humanresource;
        ```

### fine-grained access contol

it allows db admin to manage access in the very detailed level

- used to control and manage access permissions for various users and roles
- contains detailed access policies
- column level security access control
    ```sql
        GRANT SELECT (column1, column2)  ON tablename to user1;
    ```
- row level security access control
    ```sql
        CREATE RLS POLICY view_own_warehouse_inventory
            WITH (warehouse_id INTEGER)
            USING (
                warehouse_id IN (
                    SELECT managed_warehouse_id
                        FROM warehouse_managers
                        WHERE manager_username = curren_user 
                )
    ```

- masking policy

    ```sql
            CREATE MASKING POLICY mask_email
            WITH (email VARCHAR(256)
            USING ('***'::TEXT);
  
            ATTACH MASKING POLICY mask_email
            ON employe_data(email)
            TO role role_hr
            PRIORITy 20;
       ```

[<<Home page](./../README.MD#redshift-datawarehouse)