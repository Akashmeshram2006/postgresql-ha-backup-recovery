import subprocess
import time
from datetime import datetime, timezone

NODES = ["patroni-pg1", "patroni-pg3"]
OLD_PRIMARY = "patroni-pg2"

def run_command(command):
    return subprocess.run(
        command,
        capture_output=True,
        text=True
    )

def find_writable_primary():
    for node in NODES:
        result = run_command([
            "docker", "exec", node,
            "psql", "-U", "postgres", "-d", "postgres",
            "-tAc",
            "SELECT pg_is_in_recovery();"
        ])

        if result.returncode == 0 and result.stdout.strip() == "f":
            return node

    return None

print("RTO measurement: controlled primary failure")
print("Current primary:", OLD_PRIMARY)
print("Candidate nodes:", ", ".join(NODES))

input("Press ENTER to start the test...")

start = time.perf_counter()
failure_time = datetime.now(timezone.utc)

print("Stopping old primary:", OLD_PRIMARY)

stop_result = run_command(["docker", "stop", OLD_PRIMARY])

if stop_result.returncode != 0:
    print("Could not stop the old primary.")
    print(stop_result.stderr)
    raise SystemExit(1)

print("Old primary stopped. Waiting for a new writable primary...")

while True:
    new_primary = find_writable_primary()

    if new_primary:
        write_result = run_command([
            "docker", "exec", new_primary,
            "psql", "-U", "postgres", "-d", "postgres",
            "-c",
            "INSERT INTO rto_measurement (test_note) "
            "VALUES ('RTO test write after failover');"
        ])

        if write_result.returncode == 0:
            end = time.perf_counter()
            recovery_time = datetime.now(timezone.utc)

            print("\nSUCCESS: Write completed on", new_primary)
            print("Failure timestamp:", failure_time.isoformat())
            print("Successful write timestamp:", recovery_time.isoformat())
            print(f"Observed RTO: {end - start:.3f} seconds")
            break

    time.sleep(0.2)
