# other storage

### EBS (elastic block storage)

- scalable on the fly without any downtime, persistent, availability (redundancy is built in), 99,999% durability
- usually plugged to EC2 instances
- operates at block level (provides granular control over the data storage and access) so we can tailor (adapter)
  everything very specifically
- data is replicated within an availability zone (so we are protected against hardware failure)
- but EBS is also bounded to an availability zone (limited)
- one to one relationship to an ec2 (an EBS can be plugged to just one EC2)
- uses snapshot to back up data, then can use it to restore data
- high performance
- provides ability to encrypt data both at rest and transit between an instance
- cost effective (elastic) pay as you go pricing
- work around :
    - to attach it to a new instance within another AZ (account), we have to create a snapshot then bring that to the
      destination
- provisioning EBS snapshots :
    - backing up (export snapshot at specific state of our volume),
    - incremental backups (only the blocks that have changed since our last backup)
    - backups operate at block level (they capture all the data blocks, metadata, configuration settings that are
      associated)
    - before creating snapshot, for consistency reason, IO operation is locked before starting to back up
    - s3 compatible backups, compressed , encrypted at rest
    - uses lifecycle policies for the snapshots, and can be enable an automation of its management such as retention,
      deletion, copy to another AZ
    - can create a new EBS volume from the snapshot
- capacity provisioning :
    - define size of the volume or different settings such as IOPS (input/output per second)
    - different type of volumes
        - SSD GP2/GP3 (general purpose) can upgrade from GP2 to GP3 (for lower cost and higher perf)
        - IOPS optimized SSD, optimized HDD, ST1, Magnetic (infrequent access)
    - cloudwatch to monitor different metrics, such as volume read write operations, latency, queue length ...
    - delete on termination (attribute) referring to whether the volume should be deleted when the associated ECS is
      terminated
- hands on :
    - ec2 dashboard > ubuntu > t2 micro > key pair > EBS volume
    - or directly create a new volume in the same AZ as the target EC2 > attach to EC2 (note volume should be detached
      from any running ec2 for us to be able to attach to another ec2)

Note :

- root EBS is the one used as system in EC2 (/dev/sda1)
- delete on termination is set when provisioning the EC2 but cannot be changed afterwards

### EFS (elastic file system)

serverless file system, we can share files without provisioning or managing capacity and performance

- multi-availability-zone
- very scalable
- shared file system (can be plugged to multiple EC2 in the same time)
- broad range of compatibility (because use protocol NFS v4.1)
- performance mode :
    - General Purpose (broad range) (already low latency and good throughput)
        - use cases : web serving, content management, development environments
        - automatically scales performance based on data amount in the file system
    - Max I/O (high throughput / IOPS) (higher IOPS and latency insensitive and I/O intensive workloads)
        - ideal for big data analytics, media processing, database workloads
        - manually scaling
- 2 throughput modes :
    - bursting throughput mode (designed for workloads with unpredictable or spikey access patterns)
        - provides burst credits enabling burst workloads to achieve high performance
        - suitable for applications with intermittent usage patterns, such as periodic data processing tasks
    - provisioned throughput mode (designed for predictable or sustained throughput requirements)
        - user can provision a specific amount of throughput (in MB/S) for the file system
        - suitable for application with continuous data processing
- pay as you go (consumption based pricing : storage needed and data transfer)
- data security :
    - encrypted (can use KMS, option of rotating keys in a regula interval)
- POSIX System Standard API (Portable Operating System Interface) : set of apis for compatibility of UNIX-based OS
- performance :
    - autoscaling
    - 1000 NFS (network file system ) client supported
    - flexible throughput and can be adapted according to our needs
- different storage classes :
    - standard storage class
    - Infrequent Access classes (IA / One Zone IA)

### AWS Backup

- allows to configure and manage backups in one centralized place (create different back up policies and apply to
  different services EC2, RDS, EFS ... )
- automated backup scheduling, and retention too, retention rules can be configured
- cross-region and cross-account backup capabilities (important for disaster recovery)
- can restore individual files, directories or entire system depending on the service and the nature of the backup
- integrates with IAM so access to the backups can be managed
- monitor status of backups and detailed reports of backups
- how to get started ?
    - define a backup plan/ frequency / retention period
    - select the resources to include to the backup
    - monitor the back up through the management console (aws backup stores the data into an internal s3 bucket)
- aws backup vault lock
    - backup vault is a container where backups are stored securely
    - we can create multiple vault to better organize your backups like based on different criteria such as department
      application
    - so aws backup vault lock help to enhance security and compliance of backups because it allows to apply immutable
      and compliant safeguards on the backup that are stored in the backup vault
        - e.g. for compliance use case to prevent for accidentally or malicious deleting of backup
        - so once the lock is applied, no one can modify anything inside vault until the period is due, not even root
          user
    - 2 different types of vault lock modes
        - compliance mode : policy cannot be changed or deleted for the duration of the lock period
        - governance mode : allows IAM roles to manage and update vault policies but still protect from deletion
- hand-son :
    - create new backup plan > select the template > frequency > lifecycle (warm storage/or cold storage) > retention
      period > region
    - resource assignment (select which resource to bucket)
    - once created we can add up some resources to the resources assignment

[<<Home page](./../README.MD#other-storage)