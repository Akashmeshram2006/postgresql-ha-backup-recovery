# Day 13 — Primary to Replica 1

## Objective

Convert pg2 into a physical streaming replica of pg1.

## Initial State

pg2 was an independent PostgreSQL server.

```sql
SELECT pg_is_in_recovery();
