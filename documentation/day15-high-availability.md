# Day 15 — Understanding High Availability

## Objective

Understand the concepts required to convert the PostgreSQL replication
cluster into a highly available PostgreSQL system.

## High Availability

High Availability is the ability of a system to continue providing service
despite failures of individual components.

## Current PostgreSQL Cluster

```text
PG1 → Primary
PG2 → Replica
PG3 → Replica
