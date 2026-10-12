# Day 33 — Replica Recovery Test

## Objective

Verify that a failed PostgreSQL replica can rejoin the HA cluster and catch up with changes made while it was offline.

## Initial Failure

PG1 was stopped during the Day 32 replica-failure test. During its absence, PG3 remained the leader, and PG2 continued streaming replication.

## Recovery Procedure

Started the existing PG1 container:

    docker start patroni-pg1

No container or database volume was recreated.

## Cluster Verification

After restarting PG1, Patroni reported:

| Node | Role | State | Timeline | Lag |
|---|---|---|---|---|
| PG1 | Replica | Streaming | 11 | 0 |
| PG2 | Replica | Streaming | 11 | 0 |
| PG3 | Leader | Running | 11 | — |

## Data Verification

Queried the `day32_replica_test` table on PG1.

Both rows were present:

1. Write succeeded while PG1 replica was stopped
2. Second write while PG1 is stopped

The records had timestamps of `2026-10-11 07:42:47 UTC` and `2026-10-11 07:43:38 UTC`.

## Results

- PG1 restarted successfully.
- Patroni recognized PG1 as a replica.
- Streaming replication resumed.
- Both test rows were present on PG1.
- All three nodes were on timeline 11.
- Zero replication lag was reported at the time of the cluster check.

## Conclusion

The replica-recovery test passed. PG1 rejoined the cluster and caught up with the changes made while it was offline.

This test verifies recovery from a single replica failure. It does not, by itself, prove zero data loss under every possible primary or network failure scenario.
