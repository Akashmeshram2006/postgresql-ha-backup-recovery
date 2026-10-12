# Day 38 — End-to-End Integration Verification

**Date:** 12 October 2026
**Project:** PostgreSQL High Availability and Backup/Recovery

## 1. Objective

Verify that the PostgreSQL HA cluster, Patroni, etcd, pgBackRest, and MinIO backup storage are integrated and functioning.

## 2. PostgreSQL HA Cluster

Command:
`docker exec -u postgres patroni-pg1 patronictl -c /etc/patroni.yml list`

Observed result:
- pg1: Leader, running, timeline 15.
- pg2: Replica, streaming, timeline 15, reported lag 0.
- pg3: Replica, streaming, timeline 15, reported lag 0.

Result: PASS — one leader and two streaming replicas were observed.

## 3. Primary Database Connectivity

Command:
`docker exec -u postgres patroni-pg1 psql -d college_db -c "SELECT current_timestamp, pg_is_in_recovery();"`

Observed result:
- Query completed successfully.
- `pg_is_in_recovery()` returned false.

Result: PASS — pg1 was acting as the primary when tested.

## 4. pgBackRest Verification

Command:
`docker exec -u postgres patroni-pg1 pgbackrest --stanza=postgres-ha check`

Observed result:
- Repository configuration check succeeded.
- WAL archive check succeeded.
- WAL segment `0000000F0000000000000018` was archived successfully.

The `pgbackrest info` command reported:
- Stanza status: ok.
- Two full backups.
- Four differential backups.
- Archived WAL range reported from `000000080000000000000007` through `0000000F0000000000000018`.

Result: PASS — pgBackRest repository checks succeeded and backup metadata was available.

## 5. MinIO Object Storage

Command:
`mc --insecure ls --recursive local/postgres-backups/pgbackrest/`

Observed result:
- Repository objects were listed under the pgBackRest prefix.
- Objects included archived WAL segments and backup-history files.

Result: PASS — repository objects were visible in MinIO.

## 6. Overall Result

The integration checks completed successfully on 12 October 2026. At the time of testing, the cluster had one leader, two streaming replicas with zero reported lag, a working pgBackRest repository check, and visible repository objects in MinIO.

## 7. Limitations

- These checks represent one observation, not a guarantee of continuous availability.
- Listing repository objects does not independently prove that every backup is restorable.
- Restore and failure-recovery evidence is documented in the earlier Day 27 and Days 30–35 reports.
- MinIO currently uses one drive in one pool; it is not a redundant object-storage deployment.
- All database and coordination containers run in the same local Docker/WSL environment, not on independent physical hosts.
- This verification did not perform a new failover or restore.

## 8. Conclusion

The PostgreSQL HA and backup components passed the integration checks performed for Day 38. The project is ready for final scenario review and documentation, while retaining the limitations listed above.
