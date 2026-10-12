# Day 11 — PostgreSQL Host-Based Authentication

## Objective

Configure PostgreSQL authentication so replicas can connect to the primary.

## Configuration File

Inside the PostgreSQL container:

```text
/var/lib/postgresql/data/pg_hba.conf
