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
        - share setup : use named sesources or LF-tags for easy database and table sharing accross AWS accounts
        - granular access : use data filters to control access at the row and cell levers in shared tables
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

## emr

[<<Home page](./../README.MD#emr)