# Day 30 — Accidental Deletion and Recovery Test

## Objective
Verify recovery of a deleted PostgreSQL table from a pgBackRest backup.

## Backup Details
- Tool: pgBackRest
- Stanza: postgres-ha
- Type: Full
- Backup label: 20261006-092145F
- Backup date: 2026-10-06

## Failure Simulation
The students table was deleted using DROP TABLE students CASCADE. The deletion propagated to the replicas, demonstrating that replication alone does not protect against accidental logical deletion.

## Recovery
The backup was restored in an isolated recovery environment, not over the live Patroni cluster.

## Verification Results
| Table | Restored rows |
|---|---:|
| students | 20 |
| faculty | 5 |
| courses | 8 |
| marks | 40 |

The students table and its foreign-key constraints were present after recovery.

## Conclusion
The isolated recovery test succeeded. Backups provide a recovery path for accidental deletion, while high availability helps maintain service during node failures.

## Safety Notes
- The live cluster was not overwritten.
- The live students table was intentionally left deleted.
- The recovery container and volume were retained as test evidence.
