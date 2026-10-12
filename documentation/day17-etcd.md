# Day 17 — etcd Distributed Coordination Service

## Objective

The objective of Day 17 was to understand etcd and deploy a three-node etcd cluster for use as the distributed configuration store (DCS) for the PostgreSQL HA system.

## What is etcd?

etcd is a distributed key-value store designed to provide reliable and consistent storage of small amounts of critical cluster information.

In this PostgreSQL HA project, etcd is used by Patroni to coordinate the PostgreSQL cluster.

PostgreSQL itself handles data storage and streaming replication, while etcd provides the distributed coordination required by Patroni.

## Why is etcd Required?

In an HA environment, Patroni needs a reliable way for PostgreSQL nodes to agree about information such as:

* Which node is currently the leader
* Which nodes are members of the cluster
* Leader ownership information
* Cluster state
* Failover coordination

etcd provides this distributed state.

Without a DCS such as etcd, multiple PostgreSQL nodes could potentially make conflicting decisions about who should become the leader.

## Three-Node etcd Cluster

For this project, a three-node etcd cluster was created:

```text
              ┌─────────────┐
              │    etcd1    │
              └──────┬──────┘
                     │
             ┌───────┴───────┐
             │               │
             ▼               ▼
       ┌──────────┐    ┌──────────┐
       │  etcd2   │    │  etcd3   │
       └──────────┘    └──────────┘
```

The three members are:

* etcd1
* etcd2
* etcd3

A three-node cluster allows a majority of members to remain available even if one member fails.

The majority required is:

```text
3 members → quorum = 2
```

## etcd Ports

The etcd cluster uses:

| Port | Purpose                    |
| ---- | -------------------------- |
| 2379 | Client communication       |
| 2380 | Peer-to-peer communication |

Port 2379 is used by clients such as Patroni to communicate with etcd.

Port 2380 is used for communication between etcd members.

## Docker Deployment

The etcd nodes were deployed using Docker Compose.

All three etcd containers were connected to
