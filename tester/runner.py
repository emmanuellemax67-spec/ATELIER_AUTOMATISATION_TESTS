
import time
from statistics import mean

from tester.tests import (
test_latest_eur_status,
test_latest_eur_json,
test_latest_eur_schema,
test_latest_eur_types,
test_eur_usd_rate,
test_currencies,
test_historical_rate,
)

TESTS = [
test_latest_eur_status,
test_latest_eur_json,
test_latest_eur_schema,
test_latest_eur_types,
test_eur_usd_rate,
test_currencies,
test_historical_rate,
]

def percentile95(values):
"""Calcule le percentile 95 d'une liste de latences."""
if not values:
return 0

```
ordered = sorted(values)
index = max(0, int(0.95 * len(ordered) + 0.5) - 1)
return round(ordered[index], 2)
```

def run_tests():
results = []
latencies = []

```
for test in TESTS:
    start = time.perf_counter()

    try:
        test()
        status = "PASS"
        details = "Test réussi"

    except AssertionError as exc:
        status = "FAIL"
        details = str(exc)

    except Exception as exc:
        status = "ERROR"
        details = str(exc)

    elapsed_ms = round(
        (time.perf_counter() - start) * 1000, 2
    )
    latencies.append(elapsed_ms)

    results.append({
        "name": test.__name__,
        "status": status,
        "latency_ms": elapsed_ms,
        "details": details,
    })

passed = sum(r["status"] == "PASS" for r in results)
failed = sum(r["status"] == "FAIL" for r in results)
errors = sum(r["status"] == "ERROR" for r in results)
total = len(results)

return {
    "api": "Frankfurter",
    "timestamp": time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
    ),
    "summary": {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "error_rate": round(
            (failed + errors) / total, 3
        ) if total else 0,
        "latency_ms_avg": round(mean(latencies), 2)
        if latencies else 0,
        "latency_ms_p95": percentile95(latencies),
    },
    "tests": results,
}
```

if **name** == "**main**":
import json
print(json.dumps(run_tests(), indent=2, ensure_ascii=False))
