# Week 4 Summary — Backup and Recovery

## 1. Objective

The objective of Week 4 was to implement and test a backup and recovery solution for the PostgreSQL High Availability cluster using pgBackRest and MinIO object storage.

## 2. Technologies Used

- PostgreSQL 16
- pgBackRest 2.59.2
- MinIO S3-compatible object storage
- Docker and Docker Compose
- Bash scripting and cron scheduling

## 3. Backup Architecture

pgBackRest manages PostgreSQL backups and WAL archiving. Backup files are stored in the `postgres-backups` bucket in MinIO.

The repository uses the `/pgbackrest` path and Zstandard compression.

The backup configuration uses a full-backup retention setting of two backups.

## 4. Backup Schedule

The automated backup script is configured for:

- Full backup: Sunday at 02:00
- Differential backup: Monday through Saturday at 02:00

The schedule depends on the WSL environment being running when cron is due to execute.

## 5. Backup and WAL Verification

The project successfully performed pgBackRest checks and verified that the MinIO backup repository was accessible.

Recorded full backup identifiers include:

- `20261004-085827F`
- `20261006-092145F`

WAL archiving was also checked as part of backup validation.

## 6. Restore Testing

### Day 27 — Isolated Restore Test

A backup was restored into an isolated test environment, and the `backup_test` database was recovered and checked.

### Day 30 — Recovery After Table Deletion

The `students` table in the live `college_db` database was accidentally dropped during a recovery test.

The recovery procedure was tested in a separate environment using full backup `20261006-092145F`. The recovered database was verified to contain:

- Students: 20 rows
- Faculty: 5 rows
- Courses: 8 rows
- Marks: 40 rows

The recovery test also checked the relevant foreign-key relationships.

**Important:** The recovery was performed in an isolated environment. The `students` table remains deleted from the live database; the recovery test did not restore it to the live cluster.

## 7. Limitations and Security Considerations

- The implementation runs locally using Docker and WSL; it is not a production deployment.
- MinIO currently uses a single drive and is a potential single point of failure.
- TLS certificate verification is disabled in the lab configuration because of its self-signed certificate. Production deployments should use trusted certificates and enable verification.
- Cron-based automation will not run on schedule if the WSL environment is stopped.
- Backup success does not by itself guarantee successful recovery; restore testing remains essential.

## 8. Conclusion

Week 4 established a working PostgreSQL backup and recovery workflow using pgBackRest and MinIO. Backup checks, WAL archiving validation, and isolated restore tests provided evidence that the recovery process can work under the tested conditions.

Further work should include repeated recovery drills, monitoring of backup freshness, and improvements to storage redundancy and TLS configuration before any production use.
