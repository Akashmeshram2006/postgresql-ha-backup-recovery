# Day 6 - Networking Between PostgreSQL Nodes

## Objective

Understand and test networking required for communication between the PostgreSQL HA nodes.

## Host Network

Operating system:

Ubuntu Linux (WSL2)

Host IP:

Private WSL network address (not published)

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

- net-test-1
- net-test-2

Both containers were attached to postgres-ha-net.

Communication was tested using:

```bash
ping -c 3 net-test-2
```

The test verified container-to-container communication using Docker's internal DNS and bridge networking.