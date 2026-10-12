# Week 2 Summary — PostgreSQL Replication Cluster

## Objective

Build a PostgreSQL cluster consisting of one primary and two physical
streaming replicas.

## Final Architecture

```text
                    PG1
                  PRIMARY
                 /      \
                /        \
           WAL stream   WAL stream
              /            \
             ↓              ↓
           PG2              PG3
         REPLICA          REPLICA
