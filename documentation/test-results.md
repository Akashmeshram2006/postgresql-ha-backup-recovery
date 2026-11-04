# PostgreSQL High Availability, Backup and Recovery — Test Results

**Test Date:** 4 November 2026  
**PostgreSQL Version:** 16.15  
**Architecture:** 1 Primary + 2 Replicas

## 1. Test Environment

- PostgreSQL: 16.15
- High Availability Manager: Patroni
- Distributed Configuration Store: etcd (3 nodes)
- Backup Tool: pgBackRest
- Object Storage: MinIO
- Deployment: Docker containers
- Database used for recovery testing: college_db

## 2. Test Results

| No. | Test Case | Actual Result | Status |
|---|---|---|---|
| 1 | PostgreSQL installation | Version 16.15 verified | PASS |
| 2 | Three PostgreSQL nodes | pg1, pg2 and pg3 running before failover | PASS |
| 3 | Primary and replicas | 1 primary and 2 replicas verified before failover | PASS |
| 4 | Streaming replication | Both replicas streaming before failover | PASS |
| 5 | etcd health | All 3 endpoints healthy | PASS |
| 6 | MinIO availability | MinIO container running | PASS |
| 7 | Backup repository | pgBackRest status OK | PASS |
| 8 | Backup verification | Earlier verification succeeded | PASS |
| 9 | Database restoration | Full backup restored successfully | PASS |
| 10 | WAL recovery | Archive recovery completed | PASS |
| 11 | Restored data validation | 4 tables; 73 records recovered | PASS |
| 12 | Automatic failover | pg1 stopped; pg3 automatically became Leader | PASS |
| 13 | Post-failover write | INSERT on pg3 succeeded | PASS |
| 14 | Post-failover replication | Inserted record appeared on pg2 | PASS |
| 15 | RPO controlled failover test | 10/10 acknowledged records survived; 0 missing records in this test | PASS |
| 16 | RTO controlled failover test | Successful INSERT on new primary after 4.442 seconds | PASS |
|17 | Old primary rejoin | pg1 rejoined as a streaming replica; zero lag | PASS |

## 3. Database Recovery Validation

Restored database: `college_db`

| Table | Recovered Records |
|---|---:|
| students | 20 |
| courses | 8 |
| faculty | 5 |
| marks | 40 |
| **Total** | **73** |

The database was restored from the selected pgBackRest full backup dated 6 October 2026. WAL recovery completed, and PostgreSQL became ready to accept connections.

The restored instance was verified to be out of recovery mode.

## 4. Automatic Failover Test

**Test date:** 4 November 2026

- Original primary: pg1
- Failed node: pg1
- New primary: pg3
- Remaining replica: pg2
- Timeline change: 16 to 17
- pg3 successfully accepted a database write.
- The inserted record was verified on pg2.

The observed interval between pg1 stopping and the first log confirmation of pg3 holding the leader lock was approximately 0.964 seconds. This is not a definitive application-level RTO measurement.

## 5. RPO and RTO Measurement Details

### 5.1 Recovery Point Objective (RPO)

- Inserted 10 test transactions on the primary node (pg3).
- Verified all 10 records on both replicas (pg1 and pg2) before failover.
- Both replicas replayed WAL through `0/1B059160`, beyond the recorded primary position `0/1B059128`.
- Stopped pg3 to simulate primary failure.
- Patroni automatically elected pg2 as the new primary.
- Verified all 10 test records on pg2 after failover.

**Observed result:** 10 out of 10 test records survived, with zero missing records in this controlled test.

**Note:** The cluster uses asynchronous replication. This test does not guarantee zero data loss in every possible failure scenario.

### 5.2 Recovery Time Objective (RTO)

- Stopped the old primary (pg2) using a controlled failure test.
- Patroni automatically elected pg3 as the new primary.
- Executed a test INSERT on pg3 and confirmed that it succeeded.

**Failure timestamp:** `2026-11-04T16:35:01.939402+00:00`

**Successful write timestamp:** `2026-11-04T16:35:06.381026+00:00`

**Observed RTO:** `4.442 seconds`

**Note:** This measures the time from issuing the primary-stop command until a successful database write. It is an observed result in this test environment, not a guaranteed recovery time for every workload or failure.
## 6. Conclusion

The PostgreSQL cluster, streaming replication, etcd health, MinIO availability, backup repository, database restoration, WAL recovery, controlled automatic failover, post-failover write replication and old-primary rejoin have been successfully tested.

The controlled failover tests recorded zero missing records among the 10 RPO test transactions and an observed database write-recovery time of 4.442 seconds. These are test-specific results, not universal guarantees.
**Note:** The recovery test used the selected 6 October 2026 backup. It does not establish recovery of data created after that backup.

