# Week 5 Summary — PostgreSQL HA Recovery Testing

## Overview
This week tested database recovery, replica resilience, automatic failover, data preservation, and recovery time.

## Day-by-Day Results

| Day | Test | Result |
|---|---|---|
| 29 | Created college test database | Completed |
| 30 | Accidental table deletion and backup restore | Restored successfully in isolation |
| 31 | Abrupt primary failure | Automatic failover succeeded |
| 32 | Replica failure | Writes continued while a replica was stopped |
| 33 | Replica recovery | Restarted replica caught up |
| 34 | RPO/data-loss test | All five baseline records survived this test |
| 35 | RTO test | Observed recovery interval: 129 seconds |

## Day 30 — Backup Recovery
The students table was deleted from the live database using DROP TABLE CASCADE. The deletion propagated to the replicas. An isolated restore from pgBackRest recovered the students table and its 20 rows, along with the faculty, courses, and marks data.

## Days 31–33 — Failover and Replica Recovery
The cluster promoted a replica after abrupt primary failure. A separate test confirmed that writes could continue while one replica was stopped. After restart, that replica returned to streaming replication and received the missing data.

## Day 34 — Recovery Point Objective (RPO)
Five baseline records were verified on replicas before the failover test. All five remained after promotion in this test, so no baseline records were observed lost. This single result is not a guarantee of zero data loss under all conditions.

## Day 35 — Recovery Time Objective (RTO)
The measured interval from before stopping the primary until a write succeeded after failover was 129 seconds (2 minutes 9 seconds). This is an observed lab result, not a guaranteed recovery time.

## Key Lessons
- High availability and backups solve different problems.
- Logical deletion can replicate to every node.
- Patroni can coordinate automatic leader promotion.
- Replicas need to catch up after returning from an outage.
- RPO and RTO should be measured and documented.

## Week 5 Conclusion
The planned recovery and failure-testing exercises for Days 29–35 were completed. The tests demonstrated backup-based recovery, automatic failover, replica recovery, and measurable recovery behavior.

## Next Steps
- Verify the current cluster is healthy.
- Review Week 4 and Week 5 documentation.
- Continue to the next roadmap stage after confirming the lab state.
