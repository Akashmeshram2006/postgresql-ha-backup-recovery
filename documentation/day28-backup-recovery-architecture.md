# Day 28 – Backup and Recovery Architecture

## Objective

The objective of Day 28 is to document and review the backup and recovery architecture implemented for the PostgreSQL High Availability project.

The system uses pgBackRest for PostgreSQL backup management and MinIO as the S3-compatible object storage repository.

---

## Backup Architecture

The backup architecture is:

```text
             PostgreSQL HA Cluster
              /        |        \
             /         |         \
        PG1/Patroni  PG2/Patroni  PG3/Patroni
                  |
                  | pgBackRest
                  v
             MinIO S3 Storage
                  |
                  v
          postgres-backups bucket
