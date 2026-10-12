# Day 27 – Backup Verification and Restore Test

## Objective

The objective of Day 27 was to verify that PostgreSQL backups created using pgBackRest can be successfully restored from MinIO object storage into an isolated PostgreSQL environment.

The live Patroni PostgreSQL HA cluster was not used as the restore target.

---

## Backup Repository Verification

The pgBackRest repository was verified from the Patroni PostgreSQL node.

Command:

```bash
docker exec -u postgres patroni-pg2 \
  pgbackrest --stanza=postgres-ha info
