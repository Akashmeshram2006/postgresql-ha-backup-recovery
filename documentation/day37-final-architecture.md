# Day 37 — Final Project Architecture

## 1. Project
PostgreSQL High Availability, Backup and Recovery using Docker, Patroni, etcd, pgBackRest and MinIO.

## 2. Deployed Components

### PostgreSQL
- PG1, PG2 and PG3 run PostgreSQL 16.
- Patroni manages cluster membership, leader election and failover.
- Streaming replication keeps the replicas synchronized with the leader.

### Distributed Coordination
- etcd1, etcd2 and etcd3 provide distributed coordination for Patroni.
- The three-node deployment supports a quorum-based coordination design.

### Backup and Recovery
- pgBackRest manages database backups and WAL archiving.
- MinIO provides S3-compatible object storage for the backup repository.
- Restores are tested in an isolated recovery environment.

### Monitoring
- Patroni provides cluster-state information.
- Docker stats provides resource snapshots.
- pgBackRest check verifies backup repository connectivity and WAL archiving.

## 3. Architecture Flow

Clients connect directly to the PostgreSQL node ports in the current lab.

Patroni manages the PostgreSQL cluster:
- One node is leader.
- Two nodes are replicas.
- etcd stores distributed coordination state.

PostgreSQL WAL is archived by pgBackRest to the MinIO S3-compatible repository. Backups can be restored into an isolated environment for recovery testing.

## 4. Planned Improvement
HAProxy may be added to provide a stable client connection endpoint and route connections according to the intended HA design. It is not currently documented as deployed.

## 5. Important Limitations
- MinIO currently uses one drive in one pool; object-storage redundancy has not been demonstrated.
- The cluster is running in a local Docker lab, not across independent physical hosts.
- Recovery measurements are lab observations, not production guarantees.

## 6. Verification
On 2026-10-12:
- Patroni showed one leader and two streaming replicas.
- Both replicas reported zero lag.
- pgBackRest check completed successfully.
- MinIO reported online.

## 7. Conclusion
The lab demonstrates PostgreSQL streaming replication, Patroni-managed failover, distributed coordination, WAL archiving, object-storage integration, and isolated backup restoration.
