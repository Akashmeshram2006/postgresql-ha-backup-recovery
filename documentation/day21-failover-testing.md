# Day 21 — Failover Testing and Data Consistency

## Objective

The objective of Day 21 was to repeat the automatic PostgreSQL failover test, verify that a replica is automatically promoted when the leader fails, measure the failover behavior, and verify data consistency after the failover.

## Initial Cluster State

Before the failure test, PG3 was the leader and PG1 and PG2 were replicas.

The cluster was operating with:

* 1 Leader
* 2 Replicas
* Streaming replication
* Patroni automatic failover
* etcd distributed coordination

## Failure Test

A test table named `rto_test` was created on the leader.

A record was inserted before the failure:

```text
Before Day 21 failure
```

The timestamp immediately before stopping the leader was recorded as:

```text
11:49:44.166
```

PG3 was then stopped to simulate a primary-node failure.

## Automatic Failover Result

After PG3 was stopped, Patroni automatically detected the failure and promoted PG2.

The resulting cluster state was:

| Node | Role    | State             | Timeline | Lag |
| ---- | ------- | ----------------- | -------- | --- |
| PG1  | Replica | Streaming         | 4        | 0   |
| PG2  | Leader  | Running           | 4        | —   |
| PG3  | Replica | Stopped initially | 4        | —   |

PG2 successfully became the new leader.

The PostgreSQL timeline changed to Timeline 4, demonstrating that a new primary history was created after the failover.

## Write Test After Failover

A new record was inserted on the newly promoted PG2:

```text
After Day 21 automatic failover
```

The table on the new leader contained:

```text
1  | Before Day 21 failure
34 | After Day 21 automatic failover
```

This confirmed that the newly promoted leader was able to accept writes.

## Replica Recovery

PG3 was restarted after the failover.

After rejoining the Patroni cluster, the final cluster state was:

| Node | Role    | State     | Timeline | Lag |
| ---- | ------- | --------- | -------- | --- |
| PG1  | Replica | Streaming | 4        | 0   |
| PG2  | Leader  | Running   | 4        | —   |
| PG3  | Replica | Streaming | 4        | 0   |

The cluster therefore returned to a healthy 1 Leader + 2 Replicas configuration.

## Data Consistency Test

The `rto_test` table was queried from both PG1 and PG3.

Both replicas contained the same records:

```text
1  | Before Day 21 failure
34 | After Day 21 automatic failover
```

Therefore, the data written before and after the failover was successfully replicated to both replicas.

## RTO Observation

The time between the recorded failure timestamp and the later successful write was approximately 66 seconds.

However, this should **not be recorded as the exact RTO**, because the successful-write timestamp was obtained through a manual check rather than an automated measurement of the exact moment at which the new leader became available.

A more precise RTO measurement can be implemented later using automated monitoring or Patroni/API timestamps.

## Result

Day 21 was successfully completed.

The test demonstrated:

* Automatic failure detection
* Automatic leader promotion
* PostgreSQL timeline advancement
* Successful writes after failover
* Replica rejoining
* Streaming replication after recovery
* Zero replication lag after recovery
* Data consistency across replicas

## Conclusion

The PostgreSQL HA cluster successfully handled a second simulated primary failure.

PG3 was stopped, PG2 was automatically promoted to leader, and PG1 and PG3 ultimately operated as streaming replicas of PG2.

This confirms that the Patroni-based automatic failover mechanism is functioning successfully in the three-node PostgreSQL cluster.
