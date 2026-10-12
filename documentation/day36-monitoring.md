# Day 36 — Monitoring

## Objective
Monitor PostgreSQL HA status, replication, system resources, and backup storage.

## 1. PostgreSQL HA
Patroni reported:
- PG1: Leader, running, timeline 15
- PG2: Replica, streaming, lag 0
- PG3: Replica, streaming, lag 0

## 2. System Resources
- Total RAM: 3.5 GiB
- Available RAM: 2.6 GiB
- Swap: 1 GiB total, 0 bytes used
- Root filesystem: 1007 GiB total, 11 GiB used, 945 GiB available

## 3. Container Resources
Docker stats showed low CPU usage across the containers at the time of measurement. Container memory usage ranged from approximately 21 MiB for etcd1 to 140 MiB for patroni-pg1.

## 4. Backup Verification
Command: pgbackrest --stanza=postgres-ha check

Result: Completed successfully. A WAL segment was successfully archived to the configured repository.

## 5. MinIO Verification
- Status: Online
- Buckets: 1
- Objects: 2360
- Reported free capacity: 945 GiB
- Storage configuration: One drive in one pool

## 6. Conclusion
The HA cluster, WAL archiving, pgBackRest repository, and MinIO were operational during the checks. Resource usage was low during this snapshot.

MinIO uses a single-drive lab configuration, so object-storage redundancy has not been demonstrated.
