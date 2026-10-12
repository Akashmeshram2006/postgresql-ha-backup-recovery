
# Day 28 – Backup and Recovery Architecture

## 1. Objective

Document the backup and recovery architecture implemented for the PostgreSQL High Availability project. The system uses pgBackRest to manage PostgreSQL backups and MinIO as an S3-compatible object storage repository.

## 2. Architecture

```text
             PostgreSQL HA Cluster
          +----------+----------+
          |          |          |
        PG1        PG2        PG3
          \          |          /
           \   Patroni-managed /
            \     cluster     /
                    |
                 pgBackRest
                    |
             S3-compatible API
                    |
                  MinIO
                    |
           postgres-backups bucket
```

Patroni manages PostgreSQL roles and failover. pgBackRest manages database backups and WAL archiving. MinIO stores the backup repository objects.

The database cluster and MinIO run in the local Docker/WSL lab environment.

## 3. Backup Components

### PostgreSQL and Patroni

The cluster contains three PostgreSQL nodes managed by Patroni, coordinated using a three-node etcd cluster. One node acts as leader while the other two operate as replicas. Roles may change during failover.

### pgBackRest

pgBackRest manages physical backups and WAL archiving. The configured stanza is `postgres-ha`.

The repository configuration uses:
- Repository type: S3-compatible storage
- MinIO endpoint: `minio`
- Storage port: `9000`
- Bucket: `postgres-backups`
- Repository path: `/pgbackrest`
- Compression: Zstandard (`zst`)
- Full-backup retention: 2

Credentials are kept in the local configuration and must not be committed to a public repository.

### MinIO

MinIO provides S3-compatible object storage for the pgBackRest repository. The bucket contains backup repository objects and archived WAL segments.

The current lab uses one MinIO drive in one pool. Therefore, MinIO itself is not storage-redundant and is a single point of failure for the backup repository.

## 4. Backup Strategy

The configured automation script schedules:
- Full backup: Sunday at 02:00
- Differential backup: Monday through Saturday at 02:00

Differential backups depend on a preceding full backup. Recovery must use a valid backup chain and the required WAL files.

The schedule depends on the local cron service and the WSL environment being available. It should not be treated as a production scheduling guarantee.

## 5. WAL Archiving and Verification

WAL archiving allows pgBackRest to retain PostgreSQL write-ahead log segments needed for recovery.

The repository was checked using:

```bash
docker exec -u postgres patroni-pg1 \
  pgbackrest --stanza=postgres-ha check
```

The check succeeded during project verification and confirmed that a WAL segment could be archived to the repository.

The active leader can change after failover. Confirm the current Patroni leader before running leader-specific checks.

## 6. Recovery Testing

### Isolated restore

A full backup was restored into a separate recovery environment during Day 27. The restored `backup_test` data was verified.

### Accidental deletion test

During Day 30, the `students` table was deliberately dropped from the live `college_db` database to simulate accidental deletion. The table was recovered in an isolated environment from full backup `20261006-092145F`.

The isolated recovery environment contained:
- `students`: 20 rows
- `faculty`: 5 rows
- `courses`: 8 rows
- `marks`: 40 rows

The recovered data and foreign-key constraints were verified. The live deletion was intentionally retained as evidence of the test. The isolated recovery copy was not restored over the live database.

## 7. Recovery Procedure

For a real recovery operation:

1. Identify the incident and determine the required recovery point.
2. Check the current Patroni cluster state and confirm which node is leader.
3. Verify pgBackRest stanza status, available backups, and the required WAL archive.
4. Choose an isolated recovery environment or a separately approved maintenance procedure.
5. Restore the selected backup and required WAL to the intended recovery point.
6. Validate tables, row counts, constraints, and application-level consistency.
7. Record the recovery time and any observed data loss.
8. Do not overwrite a live database until the recovery plan has been reviewed and explicitly approved.

A successful lab restore does not guarantee recovery from every possible failure.

## 8. Security and Operational Limitations

- The project runs in a local Docker/WSL lab, not across independent physical hosts or availability zones.
- MinIO currently uses one drive and is not redundant.
- TLS verification is disabled in the lab configuration because a self-signed certificate is used. Production deployment should use trusted certificates and enable verification.
- Credentials must be managed securely and excluded from Git.
- The configured retention policy is not a substitute for an independently protected backup copy.
- Cron-based automation in WSL depends on the environment being running.
- Backup and recovery procedures require monitoring and regular restore testing.

## 9. Conclusion

The project integrates Patroni-managed PostgreSQL high availability with pgBackRest backups, WAL archiving, and MinIO object storage. Verification and isolated restore exercises demonstrate the core backup and recovery workflow in a lab environment.

The implementation is an educational project and is not production-ready without further work on storage redundancy, independent backup copies, security hardening, monitoring, and operational recovery procedures.
