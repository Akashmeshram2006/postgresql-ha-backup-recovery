# Day 14 — Primary to Replica 2

## Objective

Convert pg3 into a second physical streaming replica of pg1.

## Initial State

pg3 was initially an independent PostgreSQL server.

```sql

SELECT pg_is_in_recovery();
