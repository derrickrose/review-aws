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
    - introdution of metadata tagging for custom metadata attachment ?????
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

[<<Home page](./../README.MD#s3)