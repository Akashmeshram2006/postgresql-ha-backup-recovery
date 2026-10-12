# Day 6 - Networking Between PostgreSQL Nodes

## Objective

Understand and test networking required for communication between
the PostgreSQL HA nodes.

## Host Network

Ubuntu hostname:
LAPTOP-TVSKA0A1

Host IP:
172.20.159.41

Docker default bridge:
172.17.0.0/16

## Project Docker Network

Network name:
postgres-ha-net

Driver:
bridge

Subnet:
172.18.0.0/16

Gateway:
172.18.0.1

## Network Test

Two temporary Alpine Linux containers were created:

net-test-1
net-test-2

Both containers were attached to postgres-ha-net.

Communication was tested using:

ping -c 3 net-test-2

Result:

3 packets transmitted
3 packets received
0% packet loss

Therefore, container-to-container communication and Docker
container name resolution are working correctly.

## Planned HA Nodes

pg1 - PostgreSQL Primary
pg2 - PostgreSQL Replica 1
pg3 - PostgreSQL Replica 2

Additional components will later include:

etcd1
etcd2
etcd3
haproxy
minio

## Important Note

The existing Ubuntu PostgreSQL installation currently listens on
127.0.0.1:5432.

The future HA PostgreSQL instances will run as Docker containers
on the dedicated postgres-ha-net network.
