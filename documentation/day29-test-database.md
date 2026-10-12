# Day 29 — Create Test Database

## Objective

Create a realistic college database that will be used for PostgreSQL
failure, data-loss, backup, and recovery testing during Week 5.

## Database

Database name:

college_db

## Database Schema

The database contains four relational tables:

1. faculty
2. courses
3. students
4. marks

## Data Created

| Table | Records |
|---|---:|
| faculty | 5 |
| courses | 8 |
| students | 20 |
| marks | 40 |

## Relationships

- Each course can be associated with a faculty member.
- Each mark references a student.
- Each mark references a course.

## HA Cluster State

At the end of Day 29:

| Node | Role | State | Replication Lag |
|---|---|---|---:|
| PG1 | Replica | Streaming | 0 |
| PG2 | Leader | Running | — |
| PG3 | Replica | Streaming | 0 |

Timeline: 9

## Replication Verification

The test database was verified on both replicas.

PG1:
- Students: 20
- Marks: 40

PG3:
- Students: 20
- Marks: 40

This confirms that the complete test dataset was successfully
replicated from the leader to both PostgreSQL replicas.

## Baseline State

Before starting the recovery tests, the database contains:

- 5 faculty members
- 8 courses
- 20 students
- 40 marks

This baseline will be used to measure the effects of accidental
data deletion and subsequent recovery.

## Result

Day 29 completed successfully.

The PostgreSQL HA cluster contains a realistic test database and
the complete dataset is synchronized across the leader and both
replicas.
