# Day 9 — PostgreSQL Configuration

## Objective

Understand the PostgreSQL configuration parameters required for
physical streaming replication.

## Important Settings

The following settings were inspected on pg1:

```text
listen_addresses = *
port = 5432
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
