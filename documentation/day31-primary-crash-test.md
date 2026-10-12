# Day 31 — Primary Crash Test

## Objective

Test whether the PostgreSQL HA cluster can automatically
promote a replica after an abrupt primary-node failure.

## Initial State

- Primary: PG2
- Replica: PG1
- Replica: PG3
- Timeline: 10
- Replication lag: 0 reported on both replicas

## Failure Simulation

PG2 was stopped abruptly using:

    docker stop -t 0 patroni-pg2

Crash timestamp: 2026-10-11 07:34:59 UTC

## Failover Result

Patroni promoted PG3 to Leader on timeline 11.
PG1 remained a streaming replica.

Failover observed: 2026-10-11 07:36:13 UTC

Observed crash-to-failover interval: 74 seconds.

This is the interval between the recorded crash timestamp
and the observation of the new leader, not an exact internal
promotion duration.

## Client Reconnection

A fresh client connection to PG3 through host port 5545
succeeded.

The query returned:

- Database: college_db
- Server port: 5432 inside the container
- pg_is_in_recovery(): false

This confirmed that PG3 was operating as the primary.

## Data Verification

| Table | Rows verified |
|---|---:|
| faculty | 5 |
| courses | 8 |
| marks | 40 |

The students table remained absent because of the separate
Day 30 logical-deletion test. It was restored and verified
only in an isolated recovery container.

## Replica Rejoin

PG2 was restarted and successfully rejoined as a streaming
replica. The final cluster contained one leader and two
replicas, all on timeline 11 with zero reported replication
lag.

## Conclusion

The primary crash test succeeded. Patroni promoted PG3,
client reconnection succeeded, and PG1 and PG2 returned to
streaming replica status.

The measured observation interval was 74 seconds.
