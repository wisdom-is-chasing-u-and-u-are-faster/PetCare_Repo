"""
QA Persona v2 -- auto-generated tests
Service: cloned_repo
Suite:   performance
Source:  test_strategy/plans/cloned_repo__performance.json
Generated: 2024-07-12T13:01:21.583083Z
"""
import os
from locust import HttpUser, task, between, events

SERVICE_URL = os.environ.get("SERVICE_URL", "").strip()
P95_MS_THRESHOLD = float(os.environ.get("PERF_P95_MS_THRESHOLD", "500"))
FAIL_RATIO_THRESHOLD = 0.01

class TargetUser(HttpUser):
    host = SERVICE_URL
    wait_time = between(0.5, 1.5)

    @task
    def get_root(self):
        """Default task to hit the root URL, as no specific endpoints were detected."""
        self.client.get("/", name="/")

@events.test_stop.add_listener
def enforce_thresholds(environment, **kwargs):
    """Check statistics at the end of the test run and set exit code on failure."""
    stats = environment.stats.total
    fail_ratio = stats.fail_ratio
    p95_ms = stats.get_response_time_percentile(0.95)

    if fail_ratio > FAIL_RATIO_THRESHOLD:
        print(f"Test failed: Failure ratio {fail_ratio:.2f} exceeded threshold {FAIL_RATIO_THRESHOLD:.2f}")
        environment.process_exit_code = 1

    if p95_ms and p95_ms >= P95_MS_THRESHOLD:
        print(f"Test failed: P95 response time {p95_ms:.2f}ms exceeded threshold {P95_MS_THRESHOLD:.2f}ms")
        environment.process_exit_code = 1

    if environment.process_exit_code == 0:
        print("Performance thresholds met.")
