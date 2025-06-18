# analytics

## lake formation

AWS lakeformation helps us to get up, secure and well organize our datalake.
In general it is built on top of AWS glue, meaning it can manage all of the jobs glue can do.
what it can manage :

- data collection : automate data collection to our lake
- data cataloging : automate our catalog so data can be categorized and searchable
- data preparation : some cleaning or transformation
- security and access : works alongside AWS Iam, provide a fine-grained access control to manage exactly who can
  see what specific data
- data sharing : shares data between several AWS accounts (using AWS Resource Access Manager)
- works with other AWS services Athena and Redshift
- how it works :
    - collect data from different sources (on-premises and aws storage services), we specify where it comes from
    - automates with blueprints
    - uses metadata (creation date, ...) to organize the data so it is easily findable and to use (glue crawlers, glue
      catalog)
    - we can set up cleaning and transformations (structuring data to more usable format)
    - set up very detailed security options
    - use and analyse : integrates with athena (serverless query options), redshift (with lake formation we can
      configure s3 spectrum to query directly from s3)
- different security options :
    - data filtering security : for fine-grained control to the data :
        - table level security
        - column level security
        - row level security
        - cell-level security
    - how to :
        - using tags LF-tags LF-TBAC (tag-based access control) to define permissions based on attributes :
            - attach tag to the resources, then assign/revoke specific permission to the tag
        - using IAM : -
            - role based access control
            - cross-account access
    - features :
        - share setup : use named resources or LF-tags for easy database and table sharing across AWS accounts
        - granular access : use data filters to control access at the row and cell levels in shared tables
        - permission management : leverage aws Resource Access Management to handle permissions and enable cross-account
          sharing
        - resource acceptance : once shared resources are accepted via AWS RAM, the recipient's data lake administrator
          can assign further permissions
        - resource link : establish a resource link for querying shared resources via athena and redshift spectrum in
          the recipient account (e.g. link that point to a specific files in s3)
- troubleshooting :
    - issues with permission (RAM issues)
    - IAM role misconfiguration

[<<Home page](./../README.MD#lake-formation)

## emr (elastic map reduce)

- fast, distributed data processes, suitable for big data (glue is easy to use but for heavy workloads petabytes not
  that suitable)
- uses big data framework :
    - apache hadoop, apache spark, flink, ...
- for petabytes scale processing
- migration from existing on-premise
- cluster based architecture (collection of EC2)
- pricing based on EC2 usage and hourly service rates
- security :
    - IAM, VPC, KMS
- what is apache hadoop :
    - distributed storage and processing framework (hdfs + mapreduce)
- emr cluster structure :
    - each instance within to the cluster is referred as a node
    - 3 different types of nodes that we can setup in our cluster :
        - core nodes : responsible for storing and processing data (uses HDFS and splits data into blocks and distribute
          them between the core nodes), also run the processing of the tasks
        - master node : managing the cluster, running software that coordinate the distribution of the data, execution
          of tasks and status, health
        - task nodes (optional): they do not store data, just handle additional processing of data
    - fault tolerance : if one node is not working, the task are redistributed within the remain ones, and also data in
      core nodes is also redistribute in other core nodes so that data wont be lost even a node fails
- options available :
    - traditional x86 instance
    - newer graviton-based instance (balance of compute and memory 20% cost savings)
- cluster types :
    - transient (temporary cluster), we can set up like terminate cluster once task is done, example batch job
    - long running clusters : do not terminate (may be interactive data analysis so user needs to query data while
      processing)

### emr types of storage :

- hdfs : data located on the local disks of each node, use case : temporary storage, non-persistent, high throughput
- emrfs : implementation of hdfs that allows to store on S3, persistent, cost effective, storing input and output
- local file system : regular file system that you can access on each node in the cluster
- ebs volume : can be attached, uses SSD so bit more of velocity than regular EBS volumes, they are temporary and
  would be deleted when the cluster is terminated

### different deployment options

- EMR on EKS : run open source data framework on EKS, data workloads processing on EKS (elastic kubernetes service)
    - leverage the management capabilities of kubernetes (leverage = use something to its maximum advantage)
    - provisioning clusters not needed
    - simplifies container based big data processes
- EMR serverless :
    - completely abstract away the management of all the underlying compute resources
    - automatically provision, manage and scale all of the computing environment
    - automatically releases the resources after task completion (cost effective)
    - fast job startup : for application that requires quick interaction (some interactive analysis), EMR serverless can
      also pre-initialize the resources to ensure applications are ready very quickly
    - suitable for unpredictable workloads

### emr storage and scaling

- manual scaling : can add or remove instances inside the cluster
- automatic scaling : 2 different types of automatic scaling
    - aws managed : optimized for cost and performance, emr continuously evaluates the utilization of its resources and
      adjust, this can be used for a instance fleets or instance groups (group of clusters), ( one type of instances for
      master group, one type of instances for core group)
    - custom using for example cloudwatch metrics, define specific condition (scaling policies) to trigger the
      auto-scaling

[<<Home page](./../README.MD#emr)

## apache hive

[<<Home page](./../README.MD#apache-hive)