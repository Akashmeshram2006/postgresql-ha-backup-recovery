# Day 8 - PostgreSQL Installation

## Objective

Create three independent PostgreSQL nodes using Docker containers
as the laboratory environment for the PostgreSQL HA project.

## PostgreSQL Version

PostgreSQL 16

## Nodes

pg1
    Planned role: Primary

pg2
    Planned role: Replica 1

pg3
    Planned role: Replica 2

## Docker Network

Network:
postgres-ha-net

## PostgreSQL Internal Port

5432

## Host Port Mappings

pg1:
Host 5433 -> Container 5432

pg2:
Host 5434 -> Container 5432

pg3:
Host 5435 -> Container 5432

## Database

Database:
testdb

## Verification

Each PostgreSQL container was started successfully.

PostgreSQL connectivity was tested independently on pg1, pg2
and pg3.

Docker DNS resolution between PostgreSQL containers was tested.

PostgreSQL connectivity from pg1 to pg2 and pg3 was tested.

## Important

The three PostgreSQL nodes are currently independent.

Streaming replication has NOT yet been configured.

Replication will be configured during Days 9-14.
