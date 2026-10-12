# Day 16 — Patroni Architecture

## Objective

Understand Patroni and how it provides automatic PostgreSQL
high availability.

## Patroni

Patroni is a PostgreSQL high-availability manager.

It manages PostgreSQL instances and coordinates primary and
replica roles.

## PostgreSQL Replication

PostgreSQL streaming replication is responsible for transferring
WAL from the primary to replicas.

Patroni does not replace PostgreSQL replication.

## etcd

etcd is a distributed key-value store used by Patroni as a
Distributed Configuration Store (DCS).

It stores cluster coordination information and helps Patroni
coordinate the leader.

## Architecture

etcd1
etcd2
etcd3
   |
   v
Patroni
   |
PG1 / PG2 / PG3

## Quorum

A three-node etcd cluster requires a majority of two nodes
to maintain consensus.

## Automatic Failover

If the primary PostgreSQL node fails, Patroni detects the
failure and coordinates promotion of a healthy replica.

Example:

PG1 = Primary
PG2 = Replica
PG3 = Replica

After PG1 failure:

PG2 = Primary
PG3 = Replica

## Split-Brain Prevention

Distributed coordination helps prevent multiple PostgreSQL
nodes from independently becoming primary.

## Project Goal

Use Patroni and a three-node etcd cluster to convert the
existing PostgreSQL replication setup into an automatically
managed high-availability cluster.
