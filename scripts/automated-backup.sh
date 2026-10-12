#!/bin/bash

set -e

STANZA="postgres-ha"
BACKUP_TYPE="${1:-diff}"

echo "========================================"
echo " PostgreSQL Automated Backup"
echo "========================================"
echo "Started: $(date)"

# Validate backup type
if [ "$BACKUP_TYPE" != "full" ] && [ "$BACKUP_TYPE" != "diff" ]; then
    echo "ERROR: Backup type must be 'full' or 'diff'."
    echo "Usage: $0 [full|diff]"
    exit 1
fi

echo "Requested backup type: $BACKUP_TYPE"

# Find the current Patroni leader
LEADER=""

for NODE in patroni-pg1 patroni-pg2 patroni-pg3
do
    if docker ps --format '{{.Names}}' | grep -qx "$NODE"; then

        echo "Checking $NODE for current leader..."

        LEADER=$(docker exec "$NODE" patronictl \
            -c /etc/patroni.yml list 2>/dev/null |
            awk -F'|' '$4 ~ /Leader/ {
                gsub(/ /,"",$3);
                print $3;
                exit
            }')

        if [ -n "$LEADER" ]; then
            break
        fi
    fi
done

# Make sure a leader was found
if [ -z "$LEADER" ]; then
    echo "ERROR: Could not determine Patroni leader."
    exit 1
fi

echo "Current Patroni leader: $LEADER"

# Verify that the leader container is running
if ! docker ps --format '{{.Names}}' | grep -qx "$LEADER"; then
    echo "ERROR: Leader container $LEADER is not running."
    exit 1
fi

# Run pgBackRest backup
echo "Starting $BACKUP_TYPE backup..."

docker exec "$LEADER" pgbackrest \
    --stanza="$STANZA" \
    --type="$BACKUP_TYPE" \
    backup

echo "Backup completed successfully."
echo "Finished: $(date)"
