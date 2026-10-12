# Day 12 — Write-Ahead Logging (WAL)

## Objective

Understand PostgreSQL Write-Ahead Logging and its relationship to
streaming replication.

## What is WAL?

WAL stands for Write-Ahead Log.

Before database changes are safely considered persisted, PostgreSQL records
the required information in WAL.

WAL is used for:

- Crash recovery
- Physical replication
- Maintaining database consistency

## WAL Test

Initial WAL position:

```text
0/19618F8
