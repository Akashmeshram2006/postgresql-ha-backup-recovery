# Day 32 — Replica Failure Test

## Objective

Verify that the PostgreSQL HA cluster continues accepting
writes when one replica becomes unavailable.

## Initial State

- PG3: Leader
- PG1: Replica
- PG2: Replica
- Timeline: 11
- Replication lag: 0 reported on both replicas

## Failure Simulation

PG1 was stopped abruptly using:

    docker stop -t 0 patroni-pg1

Failure-test start timestamp: 2026-10-11 07:42:09 UTC

PG1 disappeared from the cluster membership view while stopped.

## Primary Availability

PG3 remained the leader and accepted two writes into
the day32_replica_test table.

The table contained two rows after the test writes.

## Remaining Replica Verification

PG2 remained a streaming replica with zero reported lag.
The first test row was queried successfully from PG2,
confirming that the write had reached the remaining replica.

## Results

| Test | Result |
|---|---|
| PG1 stopped | Successful |
| PG3 stayed leader | Successful |
| PG2 stayed streaming | Successful |
| Primary accepted writes | Successful |
| First write visible on PG2 | Successful |
| Second write accepted | Successful |

## Conclusion

The replica-failure test passed. The failure of PG1 did not
interrupt writes on PG3, and PG2 continued receiving
replicated changes.

This test covers a single replica failure; it does not
establish behavior under primary failure or loss of etcd quorum.
