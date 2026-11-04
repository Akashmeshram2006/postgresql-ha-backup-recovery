# Day 10 — PostgreSQL Users and Roles

## Objective

Create separate PostgreSQL roles for administration, application access,
and replication.

## Roles Created

### Database Administrator

```sql
CREATE ROLE dbadmin
WITH LOGIN CREATEDB CREATEROLE
PASSWORD '<YOUR_PASSWORD>';
