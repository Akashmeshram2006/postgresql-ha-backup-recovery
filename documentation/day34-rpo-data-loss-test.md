# Day 34 — RPO and Data-Loss Test

## Objective

Measure whether committed test records survive an abrupt primary failure and automatic failover.

## Baseline

Before the test:

- PG3 was the leader.
- PG1 and PG2 were streaming replicas.
- All three nodes were on timeline 11.
- Both replicas reported zero lag.
- Five records were inserted into `day34_rpo_test`.
- All five records were verified on PG1 and PG2.

Baseline timestamp: `2026-10-11 07:57:05.881067 UTC`

Baseline WAL LSN: `0/15063968`

## Failure Simulation

The primary was stopped abruptly:

    docker stop -t 0 patroni-pg3

Patroni elected PG1 as the new leader. The cluster advanced to timeline 12.

## Data Verification

The following query was executed on PG1:

    SELECT COUNT(*) AS surviving_baseline_rows
    FROM day34_rpo_test;

Result: `5`

All five baseline records survived.

## Results

| Measurement | Result |
|---|---|
| Baseline records | 5 |
| Records after failover | 5 |
| Observed missing records | 0 |
| New leader | PG1 |
| New timeline | 12 |
| PG2 status | Streaming replica |
| PG3 recovery | Rejoined as streaming replica |
| Final replica lag reported | 0 |

## Conclusion

The test observed zero loss of the five baseline records after abrupt primary failure. Patroni elected PG1, and PG2 and PG3 returned as streaming replicas.

This result applies only to the tested scenario. It does not establish a guaranteed zero RPO because the cluster uses asynchronous replication and different failure timing can produce different outcomes.

## Issue to Investigate

PG2 logs reported a local replication connection error because `pg_hba.conf` did not permit replication connections from `127.0.0.1` for the `replicator` user. Although PG2 was shown streaming, this warning should be investigated and corrected safely.

## Evidence

- Cluster listing before failure: timeline 11, PG3 leader.
- Baseline row count on PG1 and PG2: five each.
- Baseline LSN: `0/15063968`.
- Cluster listing after failover: PG1 leader on timeline 12.
- Surviving row count: five.
- Final cluster listing: PG1 leader, PG2 and PG3 streaming replicas.
