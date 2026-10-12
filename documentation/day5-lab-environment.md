# Day 5 - Lab Environment

## Project
PostgreSQL High Availability and Backup/Recovery

## Lab Approach
The project will use Docker containers instead of multiple virtual
machines because of limited available system RAM.

The containers will simulate independent PostgreSQL nodes.

## Host Resources

CPU: 12 processors
RAM: approximately 3.5 GiB
Swap: 1 GiB
Disk: approximately 1 TB

## Container Platform

Docker Version:
29.1.3

Docker Compose Version:
2.40.3

Docker Service:
Active and running

## Docker Verification

The Docker installation was tested using:

docker run hello-world

The test completed successfully.

## Planned Containers

1. PostgreSQL Node 1 - Primary
2. PostgreSQL Node 2 - Replica
3. PostgreSQL Node 3 - Replica
4. etcd nodes - HA coordination
5. HAProxy - Connection routing
6. MinIO - Backup/object storage

## Important Note

The containers are being used as a laboratory environment to
simulate independent PostgreSQL servers/nodes. The final project
will demonstrate PostgreSQL streaming replication, automatic
failover, backup, restore, and failure testing.
