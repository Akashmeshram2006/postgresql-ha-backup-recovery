# PostgreSQL High Availability and Backup/Recovery Platform

## Project Overview

This project demonstrates a PostgreSQL high-availability environment using three PostgreSQL nodes, Patroni for cluster management and automatic failover, etcd for distributed coordination, pgBackRest for backups and recovery, and MinIO for S3-compatible object storage.

The project was built as a local learning and internship project using Docker containers on Ubuntu/WSL.

## Architecture

- **PostgreSQL:** One primary and two replicas using streaming replication.
- **Patroni:** Manages PostgreSQL cluster state and automatic failover.
- **etcd:** Three-node distributed coordination cluster.
- **pgBackRest:** Performs database backups and WAL archiving.
- **MinIO:** Stores backup and archived WAL objects through an S3-compatible interface.
- **Docker:** Runs the components as containers.

Client access currently uses published PostgreSQL node ports. HAProxy or another load balancer is not yet deployed.

## Features Demonstrated

- Three-node PostgreSQL cluster.
- Automatic primary failover and replica rejoining.
- Streaming replication and replication-lag checks.
- Full and differential backups.
- WAL archiving to MinIO.
- Isolated backup restoration.
- Accidental table-deletion recovery in a separate recovery environment.
- Primary-crash, replica-failure, RPO, and RTO testing.
- Monitoring of cluster status, container resources, backups, and object storage.

## Observed Test Results

- A primary-crash test recorded an observed recovery interval of approximately 74 seconds.
- An RTO test recorded an observed interval of 129 seconds (2 minutes 9 seconds).
- In the documented RPO test, all five baseline rows survived the tested failover.
- An isolated restore recovered the documented test database tables and row counts.

These are results from individual lab tests, not guaranteed production performance or zero data loss under all failure scenarios.

## Repository Contents

- `architecture/` — architecture notes.
- `documentation/` — daily reports, test evidence, and weekly summaries.
- `patroni/` — custom image build and cluster Compose definition.
- `scripts/` — backup automation.
- `etcd-compose.yml` — etcd cluster definition.

Local configurations containing credentials, TLS private keys, backups, logs, and the MinIO executable are excluded from Git. Sanitized example configurations are provided for the three Patroni nodes and pgBackRest. Replace placeholder credentials with your own values before using the examples. These examples document the lab setup and are not production-ready configurations.

## Limitations

- All components run on one local Docker/WSL environment, not independent physical servers.
- MinIO uses a single drive in one pool in this lab and is not itself redundant.
- HAProxy or another database connection load balancer is not deployed.
- The environment is for demonstration and learning, not production deployment.
- Recovery measurements are based on limited test runs.

## Security Note

Do not commit passwords, private keys, access keys, or real environment files. Use environment variables or a secrets manager for a more secure deployment.

## Future Improvements

- Improve setup instructions so another developer can reproduce the lab safely.
- Deploy HAProxy for a stable client connection endpoint.
- Add monitoring dashboards and alerting.
- Repeat failure tests and compare recovery measurements.
- Test the setup across separate hosts and improve storage redundancy.

## Author

**Akash Meshram**  
GitHub: [@Akashmeshram2006](https://github.com/Akashmeshram2006)

### Project

PostgreSQL High Availability and Backup & Recovery using Patroni, etcd, pgBackRest, and MinIO.

This project was developed as a hands-on learning project to explore database replication, automatic failover, backup automation, and recovery testing.
