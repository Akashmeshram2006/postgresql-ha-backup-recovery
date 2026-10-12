# Day 35 — Recovery Time Objective (RTO) Test

## 1. Objective
Measure the observed recovery interval after an abrupt failure of the PostgreSQL primary. Verify automatic failover, preservation of baseline data, and successful writes after promotion.

## 2. Initial Cluster State
- Primary: PG3
- Replicas: PG1 and PG2
- Timeline: 13
- Both replicas were streaming with zero reported lag before the test.
- A baseline record was inserted and verified on both replicas.

## 3. Failure Injection
The primary was stopped abruptly using:

```bash
docker stop -t 0 patroni-pg3
```

Start timestamp captured immediately before stopping PG3:

`1791706543`

## 4. Failover Results
Patroni automatically promoted PG1 to Leader. PG2 followed PG1 as a streaming replica.

- New leader: PG1
- New timeline: 14
- PG2: Replica, streaming
- Baseline rows remained available after promotion.
- A new write succeeded on PG1.

Successful write timestamp in PostgreSQL:

`2026-10-11 08:17:42.385083+00`

End timestamp captured after the successful write:

`1791706672`

## 5. RTO Calculation

Observed recovery interval:

`1791706672 - 1791706543 = 129 seconds`

**Observed RTO: 129 seconds (2 minutes 9 seconds).**

This measurement includes failure detection, promotion, the successful write, and measurement overhead. It is a result from one test, not a guaranteed recovery time.

## 6. Recovery of PG3
After the test, PG3 was restarted. The final Patroni listing showed:

| Node | Role | State | Timeline | Reported Lag |
|---|---|---|---|---|
| PG1 | Leader | Running | 14 | — |
| PG2 | Replica | Streaming | 14 | 0 |
| PG3 | Replica | Streaming | 14 | 0 |

All three PostgreSQL nodes were healthy in the final check.

## 7. Conclusion
The automatic failover test succeeded. After PG3 stopped, Patroni promoted PG1, the baseline data remained available, and a write succeeded on the new leader. PG2 and PG3 were subsequently confirmed as streaming replicas with zero reported lag.

## 8. Limitations and Follow-up
- Repeat the test to compare observed recovery times.
- Investigate the Patroni local replication authentication warning involving `127.0.0.1`.
- Include the measured RTO and the separate RPO test results in the final project report.
- This test does not guarantee zero data loss or the same recovery time under every failure scenario.
